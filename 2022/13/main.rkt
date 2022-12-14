#lang racket

(require json)
(require racket/file)

(define (comparator a b)
  (cond
    [(and (number? a) (number? b)) (- a b)]
    [(and (number? a) (list? b)) (comparator (list a) b)]
    [(and (list? a) (number? b)) (comparator a (list b))]
    [(and (list? a) (list? b))
     (let* ([min-len (min (length a) (length b))]
            [compare-list-res
             (foldl (lambda (x y result)
                      (if (not (= result 0))
                          result
                          (comparator x y)))
                    0
                    (take a min-len)
                    (take b min-len))])
       (if (not (= compare-list-res 0))
           compare-list-res
           (- (length a)
              (length b))))]))

(define (pairs-in-order-weight packet-pairs)
  (let ([good-cmp-results-idxs (map (lambda (pair idx)
                                      (let* ([a (first pair)]
                                             [b (second pair)]
                                             [cmp-res (comparator a b)])
                                        (if (< cmp-res 1)
                                            idx
                                            0)))
                                    packet-pairs
                                    (range 1 (+ 1 (length packet-pairs))))])
    (foldl + 0 good-cmp-results-idxs)))

(define (decode-key packet-pairs)
  (let* ([less-than-packet (lambda (packet)
                             (lambda (item)
                               (< (comparator item packet) 0)))]
         [all-packets (apply append packet-pairs)]
         [packet2 '((2))]
         [packet6 '((6))]
         [p2idx (+ 1 (length
                       (filter
                         (less-than-packet packet2)
                         all-packets)))]
         [p6idx (+ 2 (length
                       (filter
                         (less-than-packet packet6)
                         all-packets)))])
    (* p2idx p6idx)))

(define fname "input.txt")

(define packet-groups
  (map (lambda (x) (map string->jsexpr (string-split x "\n")))
       (string-split (file->string fname) "\n\n")))

(displayln (format "Task 1: ~a" (pairs-in-order-weight packet-groups)))
(displayln (format "Task 2: ~a" (decode-key packet-groups)))
