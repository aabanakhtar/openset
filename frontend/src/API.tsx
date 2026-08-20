import axios, {type AxiosInstance } from "axios"
import { Navigate, Outlet } from "react-router-dom";

const API_URL: string = "http://localhost:8000"
const api: AxiosInstance = axios.create({
  baseURL: API_URL 
});

// allows us to attach the bearer to every zingle request
api.interceptors.request.use((config) => {
  const token = sessionStorage.getItem("access_token");
  // if it exists
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  
  return config;
});

// protects certain pages from showing up if not authed
export function ProtectedRoute({isAuth}: {isAuth: ()=>boolean}) {
  if (isAuth()) {
    return <Outlet />;
  } else {
    return <Navigate to="/login" />
  }
}

export default api;