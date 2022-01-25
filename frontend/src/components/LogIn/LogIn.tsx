import React, { useCallback, useEffect, useState } from "react";
import Input from "@components/Input";
import Cookies from "universal-cookie";

const cookies = new Cookies();

const LogIn: React.FC = () => {

  // const [username, setUsername] = useState("");
  // const [password, setPassword] = useState("");

  // const handleSubmit = useCallback(
  //   (event) => {
  //     async () => {
  //     try {
  //       await userStore
  //         .LogIn({
  //         username: username,
  //         password: password
  //         })
  //       .then(result => {
  //         alert(result);
  //       });
  //     } catch (err) {}
  //   };
  //   },
  //   []
  // );
  
  // return (
  //   <div>
  //   <form onSubmit={handleSubmit}>
  //     <label>
  //       Имя пользователя:
  //       <Input type="text" onChange={e => setUsername(e.target.value)} value={username} placeholder="Введите логин" />
  //     </label>
  //     <label>
  //       Пароль:
  //       <Input type="password" onChange={e => setPassword(e.target.value)} value={password} placeholder="Введите пароль" />
  //     </label>
  //     <Input type="submit" value="Отправить" />
  //     </form>
  //     </div>
  // )

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    getSession();
  }, []);
  
  const getSession = useCallback(
    () => {
 fetch("/api/session/", {
      credentials: "same-origin",
    })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      if (isAuthenticated) {
        setIsAuthenticated(true);
      } else {
        setIsAuthenticated(false);
      }
    })
    .catch((err) => {
      console.log(err);
    });
    },
    []
  );

    const whoami = useCallback(
    () => {
 fetch("/api/whoami/", {
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "same-origin",
    })
    .then((res) => res.json())
    .then((data) => {
      console.log("You are logged in as: " + data.data);
    })
    .catch((err) => {
      console.log(err);
    });
    },
    []
  );

      const handlePasswordChange = useCallback(
    (event) => {
 setPassword(event.target.value);
    },
    []
  );

  const handleUserNameChange = useCallback(
    (event) => {
 setUsername(event.target.value);
    },
    []
  );

          const isResponseOk = useCallback(
    (response) => {
  if (response.status >= 200 && response.status <= 299) {
      return response.json();
    } else {
      throw Error(response.statusText);
    }
    },
    []
  );

  
          const login = useCallback(
    (event) => {
    fetch("/api/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": cookies.get("csrftoken"),
      },
      credentials: "same-origin",
      body: JSON.stringify({username: username, password: password}),
    })
    .then(isResponseOk)
    .then((data) => {
      console.log(data);
      setIsAuthenticated(true);
      setUsername("");
      setPassword("");
      setError("");
    })
    .catch((err) => {
      console.log(err);
      setError("Wrong username or password.");
    });
    },
    []
  );

  const logout = useCallback(
    () => {
 fetch("/api/logout/", {
      credentials: "same-origin",
    })
    .then(isResponseOk)
    .then((data) => {
      console.log(data);
      setIsAuthenticated(false);
    })
    .catch((err) => {
      console.log(err);
    });
    },
    []
  );
  
      return (
        <div className="container mt-3">
          {isAuthenticated === false && (
          <div><h1>React Cookie Auth</h1><br /><h2>Login</h2><form onSubmit={login}>
              <div className="form-group">
                <label htmlFor="username">Username</label>
                <input type="text" className="form-control" id="username" name="username" value={username} onChange={handleUserNameChange} />
              </div>
              <div className="form-group">
                <label htmlFor="username">Password</label>
                <input type="password" className="form-control" id="password" name="password" value={password} onChange={handlePasswordChange} />
                <div>
                  {error !== "" &&
                    <small className="text-danger">
                      {error}
                    </small>}
                </div>
              </div>
              <button type="submit" className="btn btn-primary">Login</button>
            </form></div>
          )}
          {isAuthenticated === true && (
           <div className="container mt-3">
        <h1>React Cookie Auth</h1>
        <p>You are logged in!</p>
        <button className="btn btn-primary mr-2" onClick={whoami}>WhoAmI</button>
        <button className="btn btn-danger" onClick={logout}>Log out</button>
            </div>
            )}
        </div> 
      );
      
    }
    // return (
    //   <div className="container mt-3">
    //     <h1>React Cookie Auth</h1>
    //     <p>You are logged in!</p>
    //     <button className="btn btn-primary mr-2" onClick={this.whoami}>WhoAmI</button>
    //     <button className="btn btn-danger" onClick={this.logout}>Log out</button>
    //   </div>
    // )
//   }
// };

export default React.memo(LogIn);