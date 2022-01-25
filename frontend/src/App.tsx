import React from "react";
import { useState, useEffect } from 'react';
import {
  BrowserRouter as Router,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";
import LogIn from "@pages/LogIn";
import MainPage from "@pages/MainPage";
import Register from "@pages/Register";
import Layout from '@hocs/Layout';

import { Provider } from 'react-redux';
import store from './store';
  
function App() {
    return (
        <Provider store={store}>
        <Router>
          <Layout>
          <Routes>
            <Route path="/" element={<MainPage/>}/>
            <Route path="/login" element={<LogIn />} />
            <Route path="/register" element={<Register />}/>
            </Routes>
          </Layout>
          </Router>
        </Provider>
  );
}

export default App;
