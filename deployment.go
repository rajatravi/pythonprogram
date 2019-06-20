package main

import ("log"
		"os/exec"
		 "os"
		 "time"
		 "fmt"
		 "strconv"
		 )
		
 func main(){
	CreateDirIfNotExist()
    deploy()
	  cleanup()
 }		
 func deploy()  {

	DIRNAME := "/home/tt/top"
  CODE_PATH := "/home/tt/current"
	TIMESTAMP :=  strconv.FormatInt(time.Now().UTC().UnixNano(), 10)
	fmt.Println(TIMESTAMP)
	REPO := "https://github.com/thockin/test.git"
	cmd := exec.Command("git", "clone", REPO, DIRNAME+"/"+TIMESTAMP)
	out, err := cmd.CombinedOutput()
	  if err != nil {
		log.Fatalf("cmd.Run() failed with %s\n", err)
	}

	fmt.Printf("combined out:\n%s\n", string(out))

  if _, err := os.Lstat(CODE_PATH); err == nil {
		os.Remove(CODE_PATH)
	} 

	error := os.Symlink(DIRNAME+"/"+TIMESTAMP, CODE_PATH)
         if error != nil {
                 fmt.Println(err)               
		 }
 } 

func CreateDirIfNotExist() {

	DIRNAME := "/home/tt/top"
	 if _, err := os.Stat(DIRNAME); os.IsNotExist(err) {
			err := os.Mkdir(DIRNAME, 0755)
			if err != nil {
			log.Fatal(err)
			}
	}
}

func cleanup() {

		DIRNAME := "/home/tt/top"
		err := os.Chdir(DIRNAME)
		if err != nil {
			log.Fatal(err)
	}
	/*cmd := exec.Command("ls", "-rt")
		cmd_new := exec.Command("head", "-n", "-3")
		reader, writer := io.Pipe()
				var buf bytes.Buffer
				cmd.Stdout = writer
				cmd_new.Stdin = reader
				cmd_new.Stdout = &buf
				cmd.Start()
				cmd_new.Start()
				cmd.Wait()
				writer.Close()
				cmd_new.Wait()
				reader.Close()
				io.Copy( os.Stdout, &buf )
				fmt.Println(buf.String())
		cmd_rm := exec.Command("rm", "-rf", buf) */
		cmd := "$(rm -rf $(ls -rt | head -n -3))"
		 fmt.Printf(cmd)
    out, err := exec.Command("bash","-c",cmd).Output()
        if err != nil {
            
            log.Fatalf("cmd.Run() failed with %s\n", err)
					}
       
			 fmt.Printf("combined out:\n%s\n", string(out))  
}	


