import { useQuery } from "@tanstack/react-query";
import { motion, AnimatePresence } from "framer-motion";
import { getBookmarks } from "@/api/opportunities";
import { OpportunityCard } from "@/components/OpportunityCard";
import { Skeleton } from "@/components/ui/Skeleton";
import { Bookmark, BookmarkX } from "lucide-react";

export function Bookmarks() {
  const { data: bookmarksData, isLoading } = useQuery({
    queryKey: ["bookmarks"],
    queryFn: getBookmarks,
  });

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl flex flex-col h-full">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
          <Bookmark className="w-8 h-8 text-primary" />
          Your Bookmarks
        </h1>
        <p className="text-muted-foreground mt-1">
          Opportunities you've saved for later.
        </p>
      </div>

      <div className="flex-1">
        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="rounded-xl border bg-card p-6 h-80 flex flex-col space-y-4">
                <div className="flex justify-between">
                  <Skeleton className="h-6 w-24 rounded-full" />
                  <Skeleton className="h-8 w-8 rounded-full" />
                </div>
                <Skeleton className="h-6 w-3/4" />
                <Skeleton className="h-4 w-1/2" />
                <div className="space-y-2 mt-4 flex-1">
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-2/3" />
                </div>
                <Skeleton className="h-10 w-full mt-auto" />
              </div>
            ))}
          </div>
        ) : bookmarksData?.length === 0 ? (
          <motion.div 
            initial={{ opacity: 0 }} animate={{ opacity: 1 }}
            className="flex flex-col items-center justify-center py-20 text-center"
          >
            <div className="w-16 h-16 rounded-full bg-secondary flex items-center justify-center mb-4">
              <BookmarkX className="w-8 h-8 text-muted-foreground" />
            </div>
            <h3 className="text-xl font-semibold mb-2">No bookmarks yet</h3>
            <p className="text-muted-foreground max-w-md">
              When you see an opportunity you like, click the bookmark icon to save it here.
            </p>
          </motion.div>
        ) : (
          <motion.div 
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
            layout
          >
            <AnimatePresence>
              {bookmarksData?.map((bookmark: any) => (
                <OpportunityCard 
                  key={bookmark.opportunity.id} 
                  opportunity={bookmark.opportunity} 
                  isBookmarked={true}
                />
              ))}
            </AnimatePresence>
          </motion.div>
        )}
      </div>
    </div>
  );
}
