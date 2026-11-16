#!/bin/sh
set -eu
cd "$(dirname "$0")"
JAR="$HOME/Downloads/Ludii-1.3.14.jar"
OUT="research/day8"
mkdir -p "$OUT/classes" "$OUT/games"
javac -cp "$JAR" -d "$OUT/classes" ember-roads/measurements/EmberBaseline.java
for entry in "Pentago:lud/board/space/line/Pentago.lud" "Quarto:lud/board/space/line/Quarto.lud" "Yavalath:lud/board/space/line/Yavalath.lud" "Camelot:lud/board/race/fill/Camelot.lud" "Santorini:lud/board/race/reach/Santorini.lud"
do
  name=${entry%%:*}
  path=${entry#*:}
  echo "=== $name ==="
  (cd "$OUT/games" && jar xf "$JAR" "$path")
  if java -cp "$OUT/classes:$JAR" EmberBaseline "$OUT/games/$path" 20 20261115 > "$OUT/${name}_baseline.txt" 2>&1
  then
    cat "$OUT/${name}_baseline.txt"
  else
    echo "FAILED: $name"
    cat "$OUT/${name}_baseline.txt"
  fi
done
