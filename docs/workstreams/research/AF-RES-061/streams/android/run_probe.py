"""Researcher auxiliary: unchanged AndroidX 1.1.0 Java with explicit platform stubs.

This is not an Android device/emulator run. Fetches the release source archive,
checks its published digest, compiles eight unchanged library classes, then uses
manual timestamps and stubs for platform services. No installation is needed.
Run: python -B docs/workstreams/research/AF-RES-061/streams/android/run_probe.py
"""
from pathlib import Path
import datetime
import hashlib
import io
import json
import subprocess
import urllib.request
import zipfile

HERE = Path(__file__).resolve().parent
BUILD = HERE / "evidence" / "probe-build"
SRC = BUILD / "src"
CLASSES = BUILD / "classes"
SRC.mkdir(parents=True, exist_ok=True)
CLASSES.mkdir(parents=True, exist_ok=True)
URL = "https://dl.google.com/dl/android/maven2/androidx/dynamicanimation/dynamicanimation/1.1.0/dynamicanimation-1.1.0-sources.jar"
EXPECTED = "d730234d4276722a13721feea2630a5aaa189d5dc11681aacc7cfe94527d7b94"
archive = urllib.request.urlopen(URL, timeout=45).read()
actual = hashlib.sha256(archive).hexdigest()
assert actual == EXPECTED, (actual, EXPECTED)
z = zipfile.ZipFile(io.BytesIO(archive))

def put(path, text):
    target = SRC / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)

source_hashes = {}
for name in ["SpringForce", "SpringAnimation", "DynamicAnimation", "AnimationHandler",
             "Force", "FloatPropertyCompat", "FloatValueHolder", "FrameCallbackScheduler"]:
    path = "androidx/dynamicanimation/animation/" + name + ".java"
    raw = z.read(path)
    target = SRC / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    source_hashes[path] = hashlib.sha256(raw).hexdigest()

# These stubs provide compilation and controlled platform inputs only. No Android
# rendering, Choreographer scheduling, Looper, screen or physical device is emulated.
put("androidx/annotation/FloatRange.java", "package androidx.annotation; public @interface FloatRange {double from() default 0; double to() default Double.MAX_VALUE; boolean fromInclusive() default true; boolean toInclusive() default true;}")
put("androidx/annotation/RestrictTo.java", "package androidx.annotation; public @interface RestrictTo {Scope[] value(); enum Scope {LIBRARY,LIBRARY_GROUP,LIBRARY_GROUP_PREFIX,TESTS,SUBCLASSES}}")
for name in ["MainThread", "VisibleForTesting"]:
    put(f"androidx/annotation/{name}.java", f"package androidx.annotation; public @interface {name} {{}}")
put("androidx/annotation/RequiresApi.java", "package androidx.annotation; public @interface RequiresApi {int value() default 1; int api() default 1;}")
put("android/annotation/SuppressLint.java", "package android.annotation; public @interface SuppressLint {String[] value();}")
for name in ["NonNull", "Nullable"]:
    put(f"org/jspecify/annotations/{name}.java", f"package org.jspecify.annotations; @java.lang.annotation.Target({{java.lang.annotation.ElementType.TYPE_USE,java.lang.annotation.ElementType.METHOD,java.lang.annotation.ElementType.PARAMETER,java.lang.annotation.ElementType.FIELD}}) public @interface {name} {{}}")
put("android/util/AndroidRuntimeException.java", "package android.util; public class AndroidRuntimeException extends RuntimeException {public AndroidRuntimeException(String s){super(s);}}")
put("android/util/FloatProperty.java", "package android.util; public abstract class FloatProperty<T> {public String getName(){return \"stub\";} public abstract Float get(T o); public abstract void setValue(T o,float v);}")
put("android/os/Build.java", "package android.os; public class Build {public static class VERSION {public static int SDK_INT=33;}}")
put("android/os/SystemClock.java", "package android.os; public class SystemClock {public static long uptimeMillis(){return 1000;}}")
put("android/os/Looper.java", "package android.os; public class Looper {public static Looper myLooper(){return new Looper();} public Thread getThread(){return Thread.currentThread();}}")
put("android/view/Choreographer.java", "package android.view; public class Choreographer {public interface FrameCallback {void doFrame(long n);} public static Choreographer getInstance(){return new Choreographer();} public void postFrameCallback(FrameCallback c){}}")
put("androidx/collection/SimpleArrayMap.java", "package androidx.collection; public class SimpleArrayMap<K,V> extends java.util.HashMap<K,V> {}")
props = ["TranslationX", "TranslationY", "TranslationZ", "ScaleX", "ScaleY", "Rotation", "RotationX", "RotationY", "X", "Y", "Z", "Alpha"]
view = "package android.view; public class View {"
for name in props:
    view += f" public float get{name}(){{return 0;}} public void set{name}(float v){{}}"
for name in ["ScrollX", "ScrollY"]:
    view += f" public int get{name}(){{return 0;}} public void set{name}(int v){{}}"
put("android/view/View.java", view + "}")
put("androidx/core/view/ViewCompat.java", "package androidx.core.view; import android.view.View; public class ViewCompat {public static float getTranslationZ(View v){return 0;} public static void setTranslationZ(View v,float x){} public static float getZ(View v){return 0;} public static void setZ(View v,float x){}}")
put("android/animation/ValueAnimator.java", """package android.animation;
public class ValueAnimator {
 public static float scale=1;
 public interface DurationScaleChangeListener {void onChanged(float scale);}
 public static DurationScaleChangeListener listener;
 public static float getDurationScale(){return scale;}
 public static boolean registerDurationScaleChangeListener(DurationScaleChangeListener l){listener=l;return true;}
 public static boolean unregisterDurationScaleChangeListener(DurationScaleChangeListener l){listener=null;return true;}
 public static void setTestScale(float x){scale=x;if(listener!=null)listener.onChanged(x);}
}
""")
put("androidx/dynamicanimation/animation/Probe.java", r'''package androidx.dynamicanimation.animation;
import java.util.Locale;
public class Probe {
 static class Manual implements FrameCallbackScheduler {
  public void postFrameCallback(Runnable r) {} public boolean isCurrentThread(){return true;}
 }
 static void row(String id,String layer,long t,double x,double v,boolean done,String note) {
  System.out.printf(Locale.ROOT,"%s,%s,%d,%.12g,%.12g,%s,%s%n",id,layer,t,x,v,done,note);
 }
 static SpringForce force(float damping) {return new SpringForce(100).setStiffness(100).setDampingRatio(damping);}
 static void raw(String id,double start,double velocity,float damping,long ms) {
  SpringForce f=force(damping); f.setValueThreshold(.75);
  DynamicAnimation.MassState s=f.updateValues(start,velocity,ms);
  row(id,"SpringForce",ms,s.mValue,s.mVelocity,f.isAtEquilibrium(s.mValue,s.mVelocity),"float_output;double_input="+start);
 }
 static SpringAnimation anim(float start,float velocity,float damping,float minVisible) {
  SpringAnimation a=new SpringAnimation(new FloatValueHolder(start),100);
  a.setSpring(force(damping));a.setStartValue(start);a.setStartVelocity(velocity);a.setMinimumVisibleChange(minVisible);a.setScheduler(new Manual());return a;
 }
 static void frames(String id,float start,float velocity,float damping,long step,long cap) {
  android.animation.ValueAnimator.scale=1;android.os.Build.VERSION.SDK_INT=33;
  SpringAnimation a=anim(start,velocity,damping,1);a.start();a.doAnimationFrame(1000);
  row(id,"SpringAnimation",0,a.mValue,a.mVelocity,!a.mRunning,"first_frame_only");
  boolean crossed=false;
  for(long t=step;t<=cap;t+=step) {
   boolean done=a.doAnimationFrame(1000+t);
   if(!crossed&&a.mValue>100){crossed=true;row(id,"SpringAnimation",t,a.mValue,a.mVelocity,done,"first_sample_above_target");}
   if(t==16||t==250||done)row(id,"SpringAnimation",t,a.mValue,a.mVelocity,done,done?"first_stop":"sample");
   if(done)return;
  }
  row(id,"SpringAnimation",cap,a.mValue,a.mVelocity,!a.mRunning,"cap");
 }
 public static void main(String[] ignored) {
  System.out.println("case_id,layer,elapsed_ms,x_px,v_px_per_s,finished_or_equilibrium,note");
  for(long t:new long[]{16,250})raw("AN-N",0,0,.5f,t);
  for(long t:new long[]{0,16,250}){raw("AN-B-double",99.9,10,1,t);raw("AN-B-float",(float)99.9,10,1,t);}
  SpringForce f=force(.5f);for(long t=1;t<=3000;t++){DynamicAnimation.MassState s=f.updateValues(0,0,t);if(s.mValue>100){row("AN-N","SpringForce",t,s.mValue,s.mVelocity,false,"first_integer_ms_above_target");break;}}
  frames("AN-N-16ms",0,0,.5f,16,3000);frames("AN-N-250ms",0,0,.5f,250,3000);frames("AN-B-16ms",99.9f,10,1,16,3000);
  frames("AUX-large-frame-3000ms",0,0,.5f,3000,3000);
  frames("AUX-strong-damping",0,0,2,16,3000);
  for(long t:new long[]{16,250})raw("AUX-strong-damping-force",0,0,2,t);
  android.animation.ValueAnimator.scale=1;SpringAnimation c=anim(0,0,.5f,1);c.start();c.doAnimationFrame(1000);c.doAnimationFrame(1016);c.animateToFinalPosition(200);c.cancel();row("AUX-cancel","SpringAnimation",16,c.mValue,c.mVelocity,!c.mRunning,"pending_target="+c.getSpring().getFinalPosition());c.animateToFinalPosition(300);c.doAnimationFrame(2000);c.doAnimationFrame(2016);row("AUX-restart","SpringAnimation",16,c.mValue,c.mVelocity,!c.mRunning,"new_target="+c.getSpring().getFinalPosition());
  for(int sdk:new int[]{32,33}){android.os.Build.VERSION.SDK_INT=sdk;android.animation.ValueAnimator.scale=0;SpringAnimation a=anim(0,0,.5f,1);a.start();a.doAnimationFrame(1000);boolean done=a.doAnimationFrame(1016);row("AUX-scale0-sdk"+sdk,"SpringAnimation",16,a.mValue,a.mVelocity,done,"observed_handler_scale="+a.getAnimationHandler().getDurationScale());}
  android.os.Build.VERSION.SDK_INT=33;android.animation.ValueAnimator.scale=1;SpringAnimation a=anim(0,0,.5f,1);a.start();a.doAnimationFrame(1000);android.animation.ValueAnimator.setTestScale(0);boolean done=a.doAnimationFrame(1016);row("AUX-scale-listener","SpringAnimation",16,a.mValue,a.mVelocity,done,"observed_handler_scale="+a.getAnimationHandler().getDurationScale());
  android.animation.ValueAnimator.scale=0;SpringAnimation u=anim(0,0,0,1);u.start();u.doAnimationFrame(1000);boolean uDone=u.doAnimationFrame(1016);row("AUX-scale0-undamped","SpringAnimation",16,u.mValue,u.mVelocity,uDone,"scale0_does_not_imply_undamped_settlement");
 }
}''')
compile_cmd = ["java", "-m", "jdk.compiler/com.sun.tools.javac.Main", "-d", str(CLASSES)] + [str(p) for p in SRC.rglob("*.java")]
compiled = subprocess.run(compile_cmd, text=True, capture_output=True)
run_cmd = ["java", "-cp", str(CLASSES), "androidx.dynamicanimation.animation.Probe"]
run = subprocess.run(run_cmd, text=True, capture_output=True) if compiled.returncode == 0 else None
receipt = {"read_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "archive_url": URL,
           "archive_sha256": actual, "unchanged_source_hashes": source_hashes,
           "compile_command": compile_cmd, "compile_exit": compiled.returncode,
           "compile_stderr": compiled.stderr, "run_command": run_cmd,
           "run_exit": run.returncode if run else None,
           "run_stderr": run.stderr if run else None,
           "evidence_class": "researcher_auxiliary_exact_source_platform_stubs",
           "limits": "No Android device, emulator, rendering, real frame scheduler or actual system setting was exercised. Stub SDK and ValueAnimator values are controlled inputs. Eight library class bodies are unchanged."}
(HERE / "evidence" / "probe-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
if run:
    (HERE / "evidence" / "probe-output.csv").write_text(run.stdout)
    print(run.stdout)
print(json.dumps({"compile_exit": compiled.returncode, "compile_stderr": compiled.stderr, "run_exit": run.returncode if run else None, "run_stderr": run.stderr if run else None}))
