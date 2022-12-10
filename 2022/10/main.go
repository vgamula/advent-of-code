package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"strconv"
	"strings"
)

func nextCRTState(crt []string, xRegister int, currentCycle int) []string {
	spritePos := xRegister % 40
	caretPos := currentCycle % 40
	if math.Abs(float64(spritePos-caretPos)) <= 1 {
		return append(crt, "#")
	} else {
		return append(crt, ".")
	}
}

func displayCRT(crt []string) {
	result := ""
	for i := 0; i < 6; i++ {
		for j := 0; j < 40; j++ {
			pos := i*40 + j
			if pos >= len(crt) {
				result += "."
			} else {
				result += crt[pos]
			}
		}
		result += "\n"
	}
	fmt.Println(result)
}

func solve(commands []string) (int, []string) {
	var crt []string
	signalStrength := 0

	currentCycle := 0
	xRegister := 1
	valueToAdd := 0
	instructionProgress := 0

	for i := 0; i < len(commands); {
		currentCycle += 1
		command := commands[i]

		if instructionProgress == 0 {
			if command == "noop" {
				instructionProgress = 1
				valueToAdd = 0
			} else {
				add_arg := strings.Split(command, " ")
				valueToAdd, _ = strconv.Atoi(add_arg[1])
				instructionProgress = 2
			}
		}

		if (currentCycle-20)%40 == 0 {
			signalStrength += currentCycle * xRegister
		}

		instructionProgress -= 1
		if instructionProgress == 0 {
			xRegister += valueToAdd
			i += 1
		}

		crt = nextCRTState(crt, xRegister, currentCycle)
	}
	return signalStrength, crt
}

func main() {
	bytesRead, _ := ioutil.ReadFile("input.txt")
	fileContent := string(bytesRead)
	commands := strings.Split(fileContent, "\n")

	signalStrength, crt := solve(commands)
	fmt.Println("Task 1:", signalStrength)
	fmt.Println("Task 2:")
	displayCRT(crt)
}
