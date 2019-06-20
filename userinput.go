package main

import "fmt"

func main() {
	fmt.Println("enter the no :")
	var input int
	fmt.Scanln(&input)
	fmt.Print(input)
	if input%2 == 0 {
		fmt.Printf(" is even\n")
	} else {
		fmt.Printf(" is odd\n")
	}
}
