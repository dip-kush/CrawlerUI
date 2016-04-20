<?php
    ob_start();
    session_start();
    if(!isset($_SESSION['Username'])){
         header("Location: login.php");     
         exit();
    }
    /*if(isset($_COOKIE['user'])){
    $cookie = $_COOKIE['user'];
     if($cookie != "deepak"){
         $error = "not a valid user";
         header("Location: error.php?error=".$error);
               exit();

     }   
        
    }
    else{
        $error = "not a valid user";
         header("Location: error.php?error=".$error);
               exit();
    // Cookie is not set
    }
    */

   echo '<!DOCTYPE html>
	<html>
	<head>
   <title></title>
   </head>
   <body> <h1>hello,'.$_SESSION["Username"].'</h1><span>welcome to the profile page</span>
   <p>you can edit your page</p>

   </body>
   </html>';

?>




