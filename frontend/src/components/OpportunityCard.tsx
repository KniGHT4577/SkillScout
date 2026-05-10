import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { ExternalLink, Bookmark, BookmarkCheck, Clock, Award, BarChart } from "lucide-react";
import { motion } from "framer-motion";
import { MotionCard, CardContent, CardFooter, CardHeader, CardTitle } from "./ui/Card";
import { Badge } from "./ui/Badge";
import { Button } from "./ui/Button";
import { createBookmark, deleteBookmark } from "@/api/opportunities";
import { useAuthStore } from "@/store/useAuthStore";
import { cn } from "@/utils/cn";

export function OpportunityCard({ opportunity, isBookmarked = false }: any) {
  const queryClient = useQueryClient();
  const { isAuthenticated } = useAuthStore();
  const [bookmarked, setBookmarked] = useState(isBookmarked);

  const toggleBookmark = useMutation({
    mutationFn: async () => {
      if (bookmarked) {
        await deleteBookmark(opportunity.id);
      } else {
        await createBookmark(opportunity.id);
      }
    },
    onSuccess: () => {
      setBookmarked(!bookmarked);
      queryClient.invalidateQueries({ queryKey: ["bookmarks"] });
    }
  });

  const handleBookmarkClick = (e: React.MouseEvent) => {
    e.preventDefault();
    if (!isAuthenticated) {
      window.location.href = "/login";
      return;
    }
    toggleBookmark.mutate();
  };

  const getDifficultyColor = (diff: str) => {
    switch (diff) {
      case "beginner": return "bg-green-500/10 text-green-500 border-green-500/20";
      case "intermediate": return "bg-yellow-500/10 text-yellow-500 border-yellow-500/20";
      case "advanced": return "bg-red-500/10 text-red-500 border-red-500/20";
      default: return "bg-gray-500/10 text-gray-400 border-gray-500/20";
    }
  };

  return (
    <MotionCard
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      layout
      className="group flex flex-col h-full bg-background/40 backdrop-blur-sm border-white/5 hover:border-white/20 transition-all duration-300"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
      
      <CardHeader className="pb-4 relative z-10">
        <div className="flex justify-between items-start gap-4 mb-2">
          <Badge variant="premium" className="capitalize">
            <Award className="w-3 h-3 mr-1" />
            {opportunity.category}
          </Badge>
          <div className="flex items-center gap-2">
            {opportunity.is_free ? (
              <Badge variant="outline" className="bg-green-500/10 text-green-500 border-green-500/20">Free</Badge>
            ) : null}
            <button
              onClick={handleBookmarkClick}
              className={cn(
                "p-1.5 rounded-full transition-colors",
                bookmarked ? "text-indigo-400 bg-indigo-500/10" : "text-muted-foreground hover:text-foreground hover:bg-white/5"
              )}
            >
              {bookmarked ? <BookmarkCheck className="w-5 h-5" /> : <Bookmark className="w-5 h-5" />}
            </button>
          </div>
        </div>
        <CardTitle className="text-xl line-clamp-2 leading-tight group-hover:text-indigo-300 transition-colors">
          {opportunity.title}
        </CardTitle>
        <p className="text-sm font-medium text-muted-foreground">{opportunity.provider}</p>
      </CardHeader>
      
      <CardContent className="flex-1 flex flex-col relative z-10 pb-4">
        <p className="text-sm text-muted-foreground/80 line-clamp-3 mb-4 flex-1">
          {opportunity.ai_summary || opportunity.description}
        </p>
        
        <div className="flex flex-wrap gap-2 mt-auto">
          {opportunity.difficulty && (
            <Badge variant="outline" className={cn("capitalize text-xs flex items-center gap-1", getDifficultyColor(opportunity.difficulty))}>
              <BarChart className="w-3 h-3" />
              {opportunity.difficulty.replace('_', ' ')}
            </Badge>
          )}
          {opportunity.estimated_duration && (
            <Badge variant="outline" className="bg-white/5 text-muted-foreground text-xs flex items-center gap-1 border-white/5">
              <Clock className="w-3 h-3" />
              {opportunity.estimated_duration}
            </Badge>
          )}
        </div>
      </CardContent>
      
      <CardFooter className="pt-4 border-t border-white/5 relative z-10">
        <Button asChild className="w-full glass hover:bg-white/10 text-foreground border-white/10 group-hover:border-indigo-500/30 transition-colors">
          <a href={opportunity.url} target="_blank" rel="noopener noreferrer" className="flex items-center justify-center gap-2">
            View Details
            <ExternalLink className="w-4 h-4" />
          </a>
        </Button>
      </CardFooter>
    </MotionCard>
  );
}
