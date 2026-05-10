import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/Button";
import { Compass, Sparkles, Zap, Shield } from "lucide-react";

export function Landing() {
  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.1, delayChildren: 0.3 }
    }
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 300, damping: 24 } }
  };

  return (
    <div className="flex flex-col items-center justify-center pt-32 pb-20 px-4 text-center">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, type: "spring" }}
        className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-secondary text-secondary-foreground text-sm font-medium mb-8 border border-white/5"
      >
        <Sparkles className="w-4 h-4 text-indigo-400" />
        <span>Discover the best free learning resources using AI</span>
      </motion.div>

      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
        className="text-5xl md:text-7xl font-extrabold tracking-tight max-w-4xl mb-6 bg-clip-text text-transparent bg-gradient-to-b from-white to-white/60"
      >
        Supercharge your career without spending a dime.
      </motion.h1>

      <motion.p
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="text-lg md:text-xl text-muted-foreground max-w-2xl mb-10"
      >
        SkillScout AI scours the web to find high-quality courses, certifications, and bootcamps. Start learning exactly what you need, curated just for you.
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.3 }}
        className="flex flex-col sm:flex-row gap-4"
      >
        <Link to="/dashboard">
          <Button size="lg" variant="premium" className="w-full sm:w-auto text-md px-8 h-12 rounded-full gap-2">
            Start Exploring
            <Compass className="w-4 h-4" />
          </Button>
        </Link>
        <Link to="/login">
          <Button size="lg" variant="outline" className="w-full sm:w-auto text-md px-8 h-12 rounded-full glass hover:bg-white/5">
            Sign In
          </Button>
        </Link>
      </motion.div>

      <motion.div
        variants={container}
        initial="hidden"
        animate="show"
        className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mt-32 text-left"
      >
        {[
          { icon: Zap, title: "Real-time Discovery", desc: "Our AI pipeline continuously searches the web for the latest free courses." },
          { icon: Sparkles, title: "Smart Summaries", desc: "Get straight to the point with AI-generated course outcomes and skills." },
          { icon: Shield, title: "Curated Quality", desc: "We filter out the noise so you only see high-quality, relevant opportunities." }
        ].map((feature, i) => (
          <motion.div key={i} variants={item} className="p-6 rounded-2xl glass border border-white/5">
            <div className="w-12 h-12 rounded-full bg-indigo-500/10 flex items-center justify-center mb-4 border border-indigo-500/20">
              <feature.icon className="w-6 h-6 text-indigo-400" />
            </div>
            <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
            <p className="text-muted-foreground">{feature.desc}</p>
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
}
