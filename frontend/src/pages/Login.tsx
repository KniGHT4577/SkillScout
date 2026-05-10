import { useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { useAuthStore } from "@/store/useAuthStore";
import { login, signup, getMe } from "@/api/auth";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Compass } from "lucide-react";

export function Login() {
  const [searchParams] = useSearchParams();
  const isSignupMode = searchParams.get("signup") === "true";
  const navigate = useNavigate();
  const setAuth = useAuthStore((state) => state.setAuth);

  const [isLogin, setIsLogin] = useState(!isSignupMode);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [error, setError] = useState("");

  const loginMutation = useMutation({
    mutationFn: login,
    onSuccess: async (data) => {
      localStorage.setItem("token", data.access_token);
      try {
        const user = await getMe();
        setAuth(user, data.access_token);
        navigate("/dashboard");
      } catch (e) {
        setError("Failed to fetch user profile.");
      }
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || "An error occurred during login.");
    }
  });

  const signupMutation = useMutation({
    mutationFn: signup,
    onSuccess: () => {
      // Auto login after signup
      loginMutation.mutate({ email, password });
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || "An error occurred during signup.");
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (isLogin) {
      loginMutation.mutate({ email, password });
    } else {
      signupMutation.mutate({ email, password, full_name: fullName });
    }
  };

  const isLoading = loginMutation.isPending || signupMutation.isPending;

  return (
    <div className="flex-1 flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.4 }}
        className="w-full max-w-md p-8 rounded-2xl glass border border-white/10"
      >
        <div className="flex flex-col items-center mb-8">
          <div className="bg-primary text-primary-foreground p-3 rounded-xl mb-4 shadow-lg border border-white/10">
            <Compass className="h-8 w-8" />
          </div>
          <h2 className="text-2xl font-bold text-center">
            {isLogin ? "Welcome back" : "Create an account"}
          </h2>
          <p className="text-sm text-muted-foreground mt-2 text-center">
            {isLogin 
              ? "Enter your credentials to access your account" 
              : "Sign up to start saving and tracking opportunities"}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {!isLogin && (
            <div className="space-y-2">
              <label className="text-sm font-medium">Full Name</label>
              <Input
                type="text"
                placeholder="John Doe"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required={!isLogin}
              />
            </div>
          )}
          <div className="space-y-2">
            <label className="text-sm font-medium">Email</label>
            <Input
              type="email"
              placeholder="name@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Password</label>
            <Input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && <p className="text-sm text-destructive">{error}</p>}

          <Button type="submit" variant="premium" className="w-full h-11 mt-4" disabled={isLoading}>
            {isLoading ? "Please wait..." : (isLogin ? "Sign In" : "Sign Up")}
          </Button>
        </form>

        <div className="mt-6 text-center text-sm">
          <span className="text-muted-foreground">
            {isLogin ? "Don't have an account? " : "Already have an account? "}
          </span>
          <button
            onClick={() => setIsLogin(!isLogin)}
            className="text-primary hover:underline font-medium"
          >
            {isLogin ? "Sign up" : "Log in"}
          </button>
        </div>
      </motion.div>
    </div>
  );
}
