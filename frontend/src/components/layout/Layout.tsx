import { ReactNode } from "react";
import { Navbar } from "./Navbar";
import { motion, AnimatePresence } from "framer-motion";
import { useLocation } from "react-router-dom";

interface LayoutProps {
  children: ReactNode;
}

export function Layout({ children }: LayoutProps) {
  const location = useLocation();

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col font-sans selection:bg-indigo-500/30 selection:text-indigo-200">
      <Navbar />
      <AnimatePresence mode="wait">
        <motion.main
          key={location.pathname}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3, ease: "circOut" }}
          className="flex-1 flex flex-col relative w-full h-full"
        >
          {/* Ambient background glow for premium feel */}
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full max-w-4xl opacity-30 pointer-events-none -z-10 overflow-hidden blur-3xl">
            <div className="absolute top-[-10%] left-[20%] w-96 h-96 bg-indigo-500/20 rounded-full mix-blend-screen" />
            <div className="absolute top-[20%] right-[10%] w-80 h-80 bg-purple-500/20 rounded-full mix-blend-screen" />
          </div>
          
          {children}
        </motion.main>
      </AnimatePresence>
    </div>
  );
}
