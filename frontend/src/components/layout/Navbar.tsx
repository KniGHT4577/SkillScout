import { Link, useLocation } from "react-router-dom";
import { useAuthStore } from "@/store/useAuthStore";
import { Button } from "@/components/ui/Button";
import { motion } from "framer-motion";
import { Compass, Search, Bookmark, LogOut, User } from "lucide-react";
import { cn } from "@/utils/cn";

export function Navbar() {
  const { isAuthenticated, user, logout } = useAuthStore();
  const location = useLocation();

  const navLinks = [
    { name: "Discover", path: "/dashboard", icon: Compass },
    { name: "Bookmarks", path: "/bookmarks", icon: Bookmark, authRequired: true },
  ];

  return (
    <motion.header 
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/60 backdrop-blur-md"
    >
      <div className="container mx-auto flex h-16 items-center px-4 md:px-6">
        <Link to="/" className="flex items-center gap-2 mr-6">
          <div className="bg-primary text-primary-foreground p-1.5 rounded-lg">
            <Compass className="h-5 w-5" />
          </div>
          <span className="font-bold text-xl tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
            SkillScout AI
          </span>
        </Link>

        <nav className="flex items-center space-x-1 flex-1">
          {navLinks.map((link) => {
            if (link.authRequired && !isAuthenticated) return null;
            const isActive = location.pathname === link.path;
            const Icon = link.icon;
            return (
              <Link
                key={link.path}
                to={link.path}
                className={cn(
                  "flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-colors relative",
                  isActive ? "text-foreground" : "text-muted-foreground hover:text-foreground"
                )}
              >
                {isActive && (
                  <motion.div
                    layoutId="navbar-indicator"
                    className="absolute inset-0 bg-secondary rounded-full -z-10"
                    transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                  />
                )}
                <Icon className="h-4 w-4" />
                {link.name}
              </Link>
            );
          })}
        </nav>

        <div className="flex items-center gap-4">
          {isAuthenticated ? (
            <div className="flex items-center gap-4">
              <div className="hidden md:flex items-center gap-2 text-sm text-muted-foreground">
                <User className="h-4 w-4" />
                <span>{user?.email}</span>
              </div>
              <Button variant="ghost" size="icon" onClick={logout} title="Log out">
                <LogOut className="h-4 w-4" />
              </Button>
            </div>
          ) : (
            <>
              <Link to="/login">
                <Button variant="ghost">Log in</Button>
              </Link>
              <Link to="/login?signup=true">
                <Button variant="premium">Sign up</Button>
              </Link>
            </>
          )}
        </div>
      </div>
    </motion.header>
  );
}
