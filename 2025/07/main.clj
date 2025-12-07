(require '[clojure.set :as set]
         '[clojure.string :as str])

(def fname "example01.txt")

(def data (->> (-> (slurp fname)
                   (str/trim)
                   (str/split #"\n"))
               (mapv vec)))

(def n (count data))
(def m (count (get data 0)))

(def all-splitters
  (memoize
   (fn [i j]
     (cond
       (or (= i n)
           (< j 0)
           (= j m))
       #{}

       (= \^ (-> data (get i) (get j)))
       (set/union
        #{[i j]}
        (all-splitters i (inc j))
        (all-splitters i (dec j)))

       :else
       (all-splitters (inc i) j)))))

(def count-timelines
  (memoize
   (fn [i j]
     (cond
       (or (= i n)
           (< j 0)
           (= j m))
       1

       (= \^ (-> data (get i) (get j)))
       (+ (count-timelines i (inc j))
          (count-timelines i (dec j)))

       :else
       (count-timelines (inc i) j)))))

(let [start-i 0
      start-j (-> data (get 0) (.indexOf \S))
      t1 (-> (all-splitters start-i start-j)
             (count))
      t2 (count-timelines start-i start-j)]
  (printf "Task 1: %d\n" t1)
  (printf "Task 2: %d\n" t2))
