import {useState } from 'react'
import {mockUsers, type User} from '../interfaces/UserInterface'


export const LoginForm = () => {
  const [formUser, setFormUser] = useState("");
  const [formPassword, setFormPassword] = useState("");
  const [isLoged, setIsLoged] = useState (false)


  const handleSubmit = (e:any) => {
    e.preventDefault(); 
    console.log(isLoged)
    if(formUser && formPassword ){
        mockUsers.forEach(user => {
            if(formUser === user.UserName && formPassword=== user.Password){
                setIsLoged(true)
                alert('Logeado exitosamente')
                console.log(isLoged)}
        });

    }
    
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Título"
        value={formUser}
        onChange={(e) => setFormUser(e.target.value)}
      />
      <input
        type="text"
        placeholder="Cuerpo"
        value={formPassword}
        onChange={(e) => setFormPassword(e.target.value)}
      />
      <button type="submit">Login</button>
    </form>
  );
};
