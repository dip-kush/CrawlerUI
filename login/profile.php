<?php
    ob_start();
    session_start();
    if(!isset($_SESSION['Username'])){
         header("Location: login.php");
         return;
    }
    
    if (isset($_GET['formsubmitted'])) {
           //echo "going great";
            
             $error = "";
            $password = "";
            if(!isset($_GET['pass'])) {
               $error = 'Please Enter Your Password ';
               header("Location: error.php?error=".$error);
               exit();
             } else {
               $password = $_GET['pass'];
                //echo $password;
             }
           
            
           if(empty($error)) {
                 if($password=="deepakkool") {
                     $cookie_name = "user";                                                 
                     $cookie_value = "deepak";                                            
                     setcookie($cookie_name, $cookie_value, time() + (30), "/"); // 86400 = 1 day              
                     header("Location: getprofile.php");
                     exit();
                  }else{
                    $error = "wrong password";
                    header("Location: error.php?error=".$error);
                    exit();
                  }     
            }
            else{
                $error = "there is some error";
                header("Location: error.php?error=".$error);
                exit();
            }
            
        

    }    
   

    

?>



<html>
<head>
<title>profile</title>

<script type="text/javascript">
	


</script>

</head>

<h1>profile1</h1>

<form action="profile.php">
<input type="password" id="pass" name="pass" placeholder="password" /><br/>
<input type="hidden" name="formsubmitted" value="TRUE" /></br>
    
<input type="submit" value="submit"/>
    


</html>


