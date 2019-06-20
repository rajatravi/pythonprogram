package main

import (
	"log"
	"os"
)
func main() {
openfile()
}

func openfile(){
   f, err := os.OpenFile("notes.txt", os.O_RDWR|os.O_CREATE, 0777)
	if err != nil {
		log.Fatal(err)
	}
	if err := f.Close(); err != nil {
		log.Fatal(err)
	}
}

SMTP Username:
AKIA3YRKRIFA7CDLOW4C
SMTP Password:
BKtQpdPx5iUhNRXzGheV59XwupWVAiJMXBTZjCMKuAsf





