(require '[clojure.string :as str])

(def fname "input.txt")

(def pairs (->> (str/split (slurp fname) #"\n")
                (map
                 (fn [line]
                   (->> (str/split line #",")
                        (map
                         (fn [part]
                           (->> (str/split part #"-")
                                (mapv #(Integer/parseInt %))))))))
                (map sort)))

(->> pairs
     (filter
      (fn [[[a b] [c d]]]
        (or (<= a c d b)
            (<= c a b d))))
     (count)
     (println "Task 1:"))

(->> pairs
     (filter
      (fn [[[a b] [c _]]]
        (<= a c b)))
     (count)
     (println "Task 2:"))
