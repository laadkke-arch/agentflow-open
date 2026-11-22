import java.nio.charset.StandardCharsets;
import java.util.HexFormat;
import org.apache.arrow.c.ArrowArray;
import org.apache.arrow.c.ArrowSchema;
import org.apache.arrow.c.Data;
import org.apache.arrow.memory.ArrowBuf;
import org.apache.arrow.memory.RootAllocator;
import org.apache.arrow.vector.LargeVarBinaryVector;
import org.apache.arrow.vector.holders.NullableLargeVarBinaryHolder;

public class JavaHolderControl {
  public static void main(String[] args) {
    try (RootAllocator allocator = new RootAllocator(64L << 20)) {
      check(allocator, false);
      check(allocator, true);
    }
  }

  private static void check(RootAllocator allocator, boolean publishCount) {
    try (LargeVarBinaryVector vector = new LargeVarBinaryVector("", allocator);
         ArrowBuf buffer = allocator.buffer(16);
         ArrowArray exported = ArrowArray.allocateNew(allocator);
         ArrowSchema schema = ArrowSchema.allocateNew(allocator)) {
      vector.allocateNew(5, 1);
      byte[] data = "hello world".getBytes(StandardCharsets.UTF_8);
      buffer.setBytes(0, data);
      NullableLargeVarBinaryHolder payload = new NullableLargeVarBinaryHolder();
      payload.isSet = 1;
      payload.start = 0;
      payload.end = data.length;
      payload.buffer = buffer;
      NullableLargeVarBinaryHolder missing = new NullableLargeVarBinaryHolder();
      missing.isSet = 0;
      vector.setSafe(0, payload);
      vector.setSafe(1, missing);
      if (publishCount) {
        vector.setValueCount(2);
      }
      int producerCount = vector.getValueCount();
      Data.exportVector(allocator, vector, null, exported, schema);
      long exportedCount = exported.snapshot().length;
      try (LargeVarBinaryVector consumer = (LargeVarBinaryVector)
           Data.importVector(allocator, exported, schema, null, false)) {
        int expectedCount = publishCount ? 2 : 0;
        int importedCount = consumer.getValueCount();
        if (producerCount != expectedCount || exportedCount != expectedCount || importedCount != expectedCount) {
          throw new IllegalStateException("row-count mismatch, expected " + expectedCount);
        }
        String tail = "null";
        if (publishCount) {
          String actual = HexFormat.of().formatHex(consumer.get(0));
          if (!actual.equals(HexFormat.of().formatHex(data)) || !consumer.isNull(1)
              || consumer.getOffsetBuffer().getLong(8) != data.length) {
            throw new IllegalStateException("wrong value, null or offset");
          }
          tail = "\"" + actual + "\"";
        }
        System.out.printf(
            "{\"explicit_count\":%b,\"producer_count\":%d,\"exported_length\":%d,"
            + "\"consumer_count\":%d,\"payload_0_hex\":%s}%n",
            publishCount, producerCount, exportedCount, importedCount, tail);
      }
    }
  }
}
