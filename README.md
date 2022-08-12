# Autenticación realizada con Django Rest Framework
Esta API fue desarrollada para el registro de una aplicación que ocupe usuarios, tiene funcionalidades como:

	1. Registro de usuario: 
   	El cual pedira datos obligatorios como: username, email y password. 
		
		{
		 “username”: “Adahack”,
		 “email”: “weisseujeicrefe-2059@yopmail.com”,
		 “password”: “Ada_hack@121”
		}
		
	2. Inicio de Sesión: 
	Una vez el usuario se haya registrado, se enviara el correo de verificación de email, por lo cual una vez se verifique, 
	podrá tener acceso ingresando su email y password.
	
		{
		 “email”: “weisseujeicrefe-2059@yopmail.com”,
		 “password”: “Ada_hack@121”
		}
		
	3. Reseteo de contraseña: 
	El inicio de sesión cuenta con tres intentos por si no recuerda el usuario la contraseña, de pasar los tres intentos, 
	la cuenta se bloqueara y debera de resetear la contraseña para la recuperación de esta. Debera ingresar su contraseña
	para que le llegue un email en el cual traera un token, el cual debera ingresarse para que permita la autenticación y 
	pueda cambiar la contraseña perfectamente, los datos que pedira son email, password, iudb64 y un token.
	
		{
		 “email”: “weisseujeicrefe-2059@yopmail.com”,
		}
		
		{
		 “password”: “Ada_hack@121”, 
		 "uidb64":Ng, 
		 "token":"b9ychv-7a303c3fe383047d8b4bbb389d92ec66"
		}
		
	4. Cambio de contraseña: 
	Si la contraseña actual que tienes no es de agrado del usuario, o por algun motivo, quiere hacer el cambio, tendra la 
	opción de hacerlo siempre y cuando este autenticado, en donde debera ingresar su password actual, nuevo password y 
	confirmación del nuevo password. 
	
		{
		 "current_password": “Ada_hack@121”, 
		 "new_password":"A@jdn345",
		 "confirm_password":"A@jdn345"
		}
		
	5. Perfil de Usuario: 
	El usuario podra crear un perfil de usuario en el cual debera de ingresar datos como primer y segundo nombre, primer y 
	segundo apellido, fecha de nacimiento, lugar de nacimiento, lugar y pais de residencia. Cuenta con la función de que al 
	ingresar la fecha de nacimiento se calculara automaticamente la edad.
		{
		 "first_name":"Juan",
		 "middle_name":"Daniel",
		 "first_surname":"Perez",
		 "second_surname":"Hernandez",
		 "birth_date":"1999-04-04",
		 "place_of_birth":"mexico",
		 "residence_place":"mexico",
		 "residence_country":"mexico"
   		}
	
