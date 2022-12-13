#lang racket

(require json)
(require racket/file)

(define (sign x)
  (cond
    [(< x 0) -1]
    [(= x 0) 0]
    [(> x 0) 1]))

(define (comparator a b)
  (cond
    [(and (number? a) (number? b)) (sign (- a b))]
    [(and (number? a) (list? b)) (comparator (list a) b)]
    [(and (list? a) (number? b)) (comparator a (list b))]
    [(and (list? a) (list? b))
     (let* ([min-len (min (length a) (length b))]
            [compare-list-res
             (foldl (lambda (x y result)
                      (if (not (= result 0)) result (comparator x y)))
                    0
                    (take a min-len)
                    (take b min-len))])
       (if (not (= compare-list-res 0))
           compare-list-res
           (sign (- (length a) (length b)))))]))

(define (pairs-in-order-weight packet-pairs)
  (let ([good-cmp-results-idxs (map (lambda (pair idx)
                                      (let* ([a (first pair)]
                                             [b (second pair)]
                                             [cmp-res (comparator a b)])
                                        (if (< cmp-res 1) idx 0)))
                                    packet-pairs
                                    (range 1 (+ 1 (length packet-pairs))))])
    (foldl + 0 good-cmp-results-idxs)))

(define (decode-key packet-pairs)
  (let* ([all-input-packets (apply append packet-pairs)]
         [packet2 (list (list 2))]
         [packet6 (list (list 6))]
         [all-packets (append all-input-packets (list packet2 packet6))]
         [all-packets-sorted
          (sort all-packets (lambda (a b) (= -1 (comparator a b))))])
    (* (+ 1 (index-of all-packets-sorted packet2))
       (+ 1 (index-of all-packets-sorted packet6)))))


(define fname "input.txt")

(define packet-groups
  (map (lambda (x) (map string->jsexpr (string-split x "\n")))
       (string-split (file->string fname) "\n\n")))

(displayln (format "Task 1: ~a" (pairs-in-order-weight packet-groups)))
(displayln (format "Task 2: ~a" (decode-key packet-groups)))
