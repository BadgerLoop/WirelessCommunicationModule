n=0
   until [ $n -ge 5 ]
   do
      go run sender.go && break  # substitute your command here
      n=$[$n+1]
      sleep 1
   done
