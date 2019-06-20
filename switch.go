package main
import "fmt"

func main() {
	
	fmt.Println("enter the no")
	var input int 
	fmt.Scanln(&input) 
	switch (input) {
	case 10:
		fmt.Println(" no is 10")
	case 20:
		fmt.Println(" no is 20")
	case 30:
		fmt.Println("no is 30")
	default:
		fmt.Println("no is default")			
		
	}
}