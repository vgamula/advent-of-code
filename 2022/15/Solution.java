import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.concurrent.atomic.AtomicLong;
import java.util.HashSet;
import java.util.regex.MatchResult;
import java.util.regex.Pattern;
import java.util.stream.IntStream;

record Point(int x, int y) {
    public String serialize() {
        return x + "_" + y;
    }

    public int manhattan(Point other) {
        return Math.abs(this.x() - other.x()) + Math.abs(this.y() - other.y());
    }
}

record Sensor(Point position, Point closestBeaconPosition) {
    public int distanceCovered() {
        return this.position().manhattan(this.closestBeaconPosition);
    }

    @Override
    public String toString() {
        return "Sensor[x=" + position().x() + ", y=" + position().y() + ", d=" + this.distanceCovered() + "]";
    }

    public ArrayList<Point> getNotCoveredPerimeterPoints() {
        var res = new ArrayList<Point>();
        var x = this.position().x();
        var y = this.position().y() + this.distanceCovered() + 1;
        while (x != this.position().x() + this.distanceCovered() + 1) {
            res.add(new Point(x, y));
            x += 1;
            y -= 1;
        }
        while (y != this.position().y() - this.distanceCovered() - 1) {
            res.add(new Point(x, y));
            x -= 1;
            y -= 1;
        }
        while (x != this.position().x() - this.distanceCovered() - 1) {
            res.add(new Point(x, y));
            x -= 1;
            y += 1;
        }
        while (y != this.position().y() + this.distanceCovered() + 1) {
            res.add(new Point(x, y));
            x += 1;
            y += 1;
        }
        return res;
    }
}

public class Solution {
    public static Sensor parseSensorReport(String s) {
        var p = Pattern.compile("-?\\d+");
        var m = p.matcher(s);
        var vals = m.results().map(MatchResult::group).mapToInt(Integer::parseInt).toArray();
        return new Sensor(new Point(vals[0], vals[1]), new Point(vals[2], vals[3]));
    }

    public static ArrayList<Sensor> loadSensorsFromFile(String fileName) throws IOException {
        var result = new ArrayList<Sensor>();
        var file = new File(fileName);
        try (var linesStream = Files.lines(file.toPath())) {
            linesStream.forEach(line -> {
                var parsedSensor = parseSensorReport(line);
                result.add(parsedSensor);
            });
        }
        return result;
    }

    public static int countNotPossibleBeaconPositionsInLine(ArrayList<Sensor> sensors, int y) {
        var minX = Integer.MAX_VALUE;
        var maxX = Integer.MIN_VALUE;
        var existingObjects = new HashSet<String>();
        for (Sensor sensor : sensors) {
            minX = Math.min(minX, sensor.position().x() - sensor.distanceCovered());
            minX = Math.min(minX, sensor.closestBeaconPosition().x());
            maxX = Math.max(maxX, sensor.position().x() + sensor.distanceCovered());
            maxX = Math.max(maxX, sensor.closestBeaconPosition().x());
            existingObjects.add(sensor.position().serialize());
            existingObjects.add(sensor.closestBeaconPosition().serialize());
        }

        var result = 0;

        for (int x = minX; x <= maxX; x++) {
            for (var s : sensors) {
                var point = new Point(x, y);
                if (point.manhattan(s.position()) <= s.distanceCovered()
                        && !existingObjects.contains(new Point(x, y).serialize())) {
                    result += 1;
                    break;
                }
            }
        }

        return result;
    }

    public static int findAndPrintTuningFrequencySuperSlow(ArrayList<Sensor> sensors) {
        var max = 4_000_000 + 1;
        var maxPointsToCheck = (long) 4_000_000 * (long) 4_000_000;
        var pointsChecked = new AtomicLong();
        var start = Instant.now();
        IntStream.range(0, max).parallel().forEach(x -> {
            IntStream.range(0, max).parallel().forEach(y -> {
                var isPointHiddenFromAllSensors = true;
                for (var s : sensors) {
                    var point = new Point(x, y);
                    if (point.manhattan(s.position()) <= s.distanceCovered()) {
                        isPointHiddenFromAllSensors = false;
                        break;
                    }
                }
                if (isPointHiddenFromAllSensors) {
                    System.out.println("found: x=" + x + ", y=" + y);
                }
                var tmp = pointsChecked.incrementAndGet();
                if (tmp % 1_000_000_000 == 0) {
                    var finish = Instant.now();
                    var timeElapsed = Duration.between(start, finish).toSeconds();
                    System.out.println(1.0 * tmp / maxPointsToCheck * 100 + ", seconds passed: " + timeElapsed);
                }
            });
        });

        return -1;
    }

    public static long findTuningFrequencyFast(ArrayList<Sensor> sensors, int limit) {
        for (var s : sensors) {
            for (var p : s.getNotCoveredPerimeterPoints()) {
                if (!(0 <= p.x() && p.x() <= limit && 0 <= p.y() && p.y() <= limit)) {
                    continue;
                }

                var isPointHiddenFromAllSensors = true;
                for (var s2 : sensors) {
                    if (p.manhattan(s2.position()) <= s2.distanceCovered()) {
                        isPointHiddenFromAllSensors = false;
                        break;
                    }
                }

                if (isPointHiddenFromAllSensors) {
                    var tuningFrequency = 4_000_000 * (long) p.x() + p.y();
                    // System.out.println("found: x=" + p.x + ", y=" + p.y);
                    return tuningFrequency;
                }
            }
        }
        return -1;
    }

    public static void main(String[] args) throws IOException {
        // var filename = "example.txt";
        // var targetY = 10;
        // var limit = 20;
        var filename = "input.txt";
        var targetY = 2000000;
        var limit = 4_000_000;
        var sensors = loadSensorsFromFile(filename);

        System.out.println("Task 1: " + countNotPossibleBeaconPositionsInLine(sensors, targetY));
        System.out.println("Task 2: " + findTuningFrequencyFast(sensors, limit));
    }
}
