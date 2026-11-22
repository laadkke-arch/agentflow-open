import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.HexFormat;
import java.util.List;
import java.util.Objects;
import org.apache.arrow.memory.ArrowBuf;
import org.apache.arrow.memory.RootAllocator;
import org.apache.arrow.vector.FieldVector;
import org.apache.arrow.vector.IntVector;
import org.apache.arrow.vector.LargeVarBinaryVector;
import org.apache.arrow.vector.VarBinaryVector;
import org.apache.arrow.vector.complex.LargeListVector;
import org.apache.arrow.vector.complex.ListVector;
import org.apache.arrow.vector.ipc.ArrowStreamReader;

public class ArrowConsumer {
  static final long LIMIT = 64L << 20;
  static final HexFormat HEX = HexFormat.of();
  static final long[] BINARY_OFFSETS = {0, 2, 2, 5};
  static final long[] LIST_OFFSETS = {0, 3, 3, 3};

  static void require(boolean condition, String name) {
    if (!condition) {
      throw new IllegalStateException(name);
    }
  }

  static long[] offsets(FieldVector vector, int width) {
    ArrowBuf buffer = vector.getOffsetBuffer();
    long[] result = new long[vector.getValueCount() + 1];
    for (int i = 0; i < result.length; i++) {
      long index = (long) width * i;
      result[i] = width == 8 ? buffer.getLong(index) : buffer.getInt(index);
    }
    return result;
  }

  public static String observe(FieldVector binary, FieldVector list, boolean large) {
    require(binary.getClass() == (large ? LargeVarBinaryVector.class : VarBinaryVector.class),
        "binary vector: " + binary.getClass().getSimpleName());
    require(list.getClass() == (large ? LargeListVector.class : ListVector.class),
        "list vector: " + list.getClass().getSimpleName());
    require(binary.getValueCount() == 3 && list.getValueCount() == 3, "row counts");
    require(binary.getNullCount() == 1 && binary.isNull(1), "binary validity");
    require(list.getNullCount() == 1 && list.isNull(1), "list validity");

    byte[] first = (byte[]) binary.getObject(0);
    byte[] last = (byte[]) binary.getObject(2);
    require(HEX.formatHex(first).equals("6162"), "first payload");
    require(binary.getObject(1) == null && HEX.formatHex(last).equals("78797a"), "last payload");
    require(Objects.equals(list.getObject(0), Arrays.asList(1, null, 2)), "list elements and child null");
    require(list.getObject(1) == null && Objects.equals(list.getObject(2), List.of()), "null and empty list");
    FieldVector data = large
        ? ((LargeListVector) list).getDataVector() : ((ListVector) list).getDataVector();
    require(data instanceof IntVector && data.getNullCount() == 1 && data.isNull(1), "Int32 child validity");

    int width = large ? 8 : 4;
    long[] binaryOffsets = offsets(binary, width);
    long[] listOffsets = offsets(list, width);
    require(Arrays.equals(binaryOffsets, BINARY_OFFSETS), "binary offsets " + Arrays.toString(binaryOffsets));
    require(Arrays.equals(listOffsets, LIST_OFFSETS), "list offsets " + Arrays.toString(listOffsets));
    return String.format(
        "{\"vectors\":[\"%s\",\"%s\"],\"offset_width_bytes\":%d,\"binary_offsets\":%s,"
        + "\"list_offsets\":%s,\"payload_hex\":[\"%s\",null,\"%s\"],\"items\":[%s,null,%s],"
        + "\"parent_nulls\":[%d,%d],\"child_nulls\":%d}",
        binary.getClass().getSimpleName(), list.getClass().getSimpleName(), width,
        Arrays.toString(binaryOffsets), Arrays.toString(listOffsets), HEX.formatHex(first), HEX.formatHex(last),
        list.getObject(0), list.getObject(2), binary.getNullCount(), list.getNullCount(), data.getNullCount());
  }

  public static void main(String[] args) throws Exception {
    if (args.length != 2 || !(args[1].equals("large") || args[1].equals("stored"))) {
      throw new IllegalArgumentException("usage: ArrowConsumer <ipc-stream> <large|stored>");
    }
    try (RootAllocator allocator = new RootAllocator(LIMIT);
         InputStream input = Files.newInputStream(Path.of(args[0]));
         ArrowStreamReader reader = new ArrowStreamReader(input, allocator)) {
      require(reader.loadNextBatch(), "first batch");
      var root = reader.getVectorSchemaRoot();
      require(root.getFieldVectors().size() == 2 && root.getRowCount() == 3, "field and row counts");
      System.out.println(observe(root.getVector("payload"), root.getVector("items"), args[1].equals("large")));
      require(!reader.loadNextBatch(), "single batch");
    }
  }
}
