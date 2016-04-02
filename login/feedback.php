<?php



include ('database_connection.php');

$name = $_GET['name'];
$fb = $_GET['fb'];

$query = "insert into feedback(name, feedback) values('$name', '$fb')";

 $result_check_credentials = mysqli_query($dbc, $query);
        if(!$result_check_credentials){//If the QUery Failed 
            echo 'Query Failed ';
        }
	else{
	    echo "<title>Form1</title> <p>feedback Submitted</p>";
        echo "<p>to submit another feedback go back</p>";
           // echo "<a href='login'>login</a>";
	}

?>
