<?php
	include 'connection.php';
	

	$first_name = $_POST['first_name'];
	$last_name = $_POST['last_name'];
	$email = $_POST['email'];
	$contact = $_POST['contact'];
	$job_func = $_POST['job_func'];
	$message = $_POST['message'];
	
	$tm=md5(time());
	$fnm=$_FILES['image']['name'];
	$dst="./admin/clientImg/".$tm.$fnm;
	$dst1="admin/clientImg/".$tm.$fnm;
	move_uploaded_file($_FILES['image']['tmp_name'],$dst);
	
		mysqli_query($link,
			"INSERT INTO `client_info` 
				VALUES(
					NULL,
					'$first_name',
					'$last_name',
					'$email',
					'$contact',
					'$job_func',
					'$message',
					'$dst1'
				)"
		);
?>