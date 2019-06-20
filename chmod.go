package main

import ("log"
		"os")
		
 func main()  {
	 chmod()
	 chmodnew()
 }		

 func chmod()  {
	 err := os.Chmod("notes.txt", 0664)
	if err != nil {
		log.Fatal(err)
	} 
 }
 func chmodnew()  {
	err := os.Mkdir("/home/tt/top", 0777)
	if err != nil {
		log.Fatal(err)
	}
}