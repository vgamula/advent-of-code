import scala.io.Source

sealed trait RelaxConfig

case class RelaxEnabled() extends RelaxConfig
case class RelaxDisabled() extends RelaxConfig

case class TestConfig(
    val divisibleBy: Long,
    val nextMonkeyIfTrue: Int,
    val nextMonkeyIfFalse: Int
);

class Monkey(
    var items: List[Long],
    val transformOperation: Array[String],
    val testConfig: TestConfig
) {
  var inspectedItemsCount: Long = 0

  def trackInspectedItems(): Unit = {
    inspectedItemsCount = inspectedItemsCount + items.length
  }
};

object Main {
  def parseMonkeyConfig(monkeyConfigStr: String): Monkey = {
    val rows = monkeyConfigStr.split("\n").map(_.trim)

    val items =
      rows(1).replace("Starting items: ", "").split(", ").map(_.toLong).toList

    val transformOperation = rows(2).replace("Operation: new = ", "").split(" ")

    val divisibleBy = rows(3).replace("Test: divisible by ", "").toLong
    val nextMonkeyIfTrue =
      rows(4).replace("If true: throw to monkey ", "").toInt
    val nextMonkeyIfFalse =
      rows(5).replace("If false: throw to monkey ", "").toInt

    new Monkey(
      items,
      transformOperation,
      TestConfig(divisibleBy, nextMonkeyIfTrue, nextMonkeyIfFalse)
    )
  }

  def setupMonkeys(config: String): Array[Monkey] = {
    config.split("\n\n").map(parseMonkeyConfig)
  }

  def solve(
      monkeys: Array[Monkey],
      relaxConfig: RelaxConfig,
      rounds: Int
  ): Long = {
    // ideally, should be replaced with LCM
    val scopeOfDivisibility = monkeys.map(_.testConfig.divisibleBy).product

    for (round <- 1 to rounds) {
      for (monkey <- monkeys) {
        monkey.trackInspectedItems()
        while (monkey.items.length > 0) {
          val item = monkey.items.head
          monkey.items = monkey.items.drop(1)

          val largeWorryLevel: Long = monkey.transformOperation match {
            case Array("old", op, "old") =>
              if (op == "+") item + item else item * item
            case Array("old", op, b) =>
              if (op == "+") item + b.toLong else item * b.toLong
          }

          val finalWorryLevel = relaxConfig match {
            case RelaxEnabled()  => (largeWorryLevel % scopeOfDivisibility) / 3
            case RelaxDisabled() => largeWorryLevel % scopeOfDivisibility
          }

          if (finalWorryLevel % monkey.testConfig.divisibleBy == 0) {
            monkeys(monkey.testConfig.nextMonkeyIfTrue).items = monkeys(
              monkey.testConfig.nextMonkeyIfTrue
            ).items ::: List(finalWorryLevel)
          } else {
            monkeys(monkey.testConfig.nextMonkeyIfFalse).items = monkeys(
              monkey.testConfig.nextMonkeyIfFalse
            ).items ::: List(finalWorryLevel)
          }
        }
      }
    }

    monkeys.map(_.inspectedItemsCount).sortWith(_ > _).take(2).product
  }

  def main(args: Array[String]): Unit = {
    val monkeysConfig = Source.fromFile("input.txt").mkString
    val monkeys = setupMonkeys(monkeysConfig)
    val task1 = solve(monkeys, RelaxEnabled(), 20)
    println(s"Task 1: $task1")

    val monkeys2 = setupMonkeys(monkeysConfig)
    val task2 = solve(monkeys2, RelaxDisabled(), 10000)
    println(s"Task 2: $task2")
  }
}
