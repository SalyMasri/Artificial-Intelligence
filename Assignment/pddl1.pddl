;; Domain definition
(define (domain travel-domain)
  
  ;; Predicates: Properties of objects that we are interested in (boolean)
  (:predicates
    (AIRPORT ?x) ; True if x is an airport
    (STATION ?x) ; True if x is a station
    (PERSON ?x) ; True if x is a person
    (VEHICLE ?x) ; True if x is a method of transportation
    (AIRPLANE ?x) ; True if x is an airplane
    (SUBWAY ?x) ; True if x is a subway
    (connected ?x ?y) ; True if airport/station x is connected to airport/station y
    (is-person-at ?x ?y) ; True if person x is at airport/station y
    (is-vehicle-at ?x ?y) ; True if vehicle x is at airport/station y
    (is-person-in-vehicle ?x ?y) ; True if person x is in vehicle y
  )
  ;; Actions: Ways of changing the state of the world
  
  ; Person x enters vehicle y if both are in the same airport/station z.
  ; As a result, person x is in vehicle y and not at z anymore.
  (:action enter-vehicle
    :parameters (?x ?y ?z)
    :precondition (and
      (PERSON ?x)
      (VEHICLE ?y)
      (or (AIRPORT ?z) (STATION ?z))
      (is-person-at ?x ?z)
      (is-vehicle-at ?y ?z)
    )
    :effect (and
      (is-person-in-vehicle ?x ?y)
      (not (is-person-at ?x ?z))
    )
  )
  
  ; Person x leaves vehicle y in airport/station z if the person x is in the 
  ; vehicle y and the vehicle y is at z.
  ; As a result, person x is not in vehicle y anymore and the person x is at z
  (:action leave-vehicle
    :parameters (?x ?y ?z)
    :precondition (and
      (PERSON ?x)
      (VEHICLE ?y)
      (or (AIRPORT ?z) (STATION ?z))
      (is-person-in-vehicle ?x ?y)
      (is-vehicle-at ?y ?z)
    )
    :effect (and
      (is-person-at ?x ?z)
      (not (is-person-in-vehicle ?x ?y))
    )
  )

  ; Long-distance travel, i.e. between airports x and y by an 
  ; airplane z if x and y are connected.
  ; As a result, vehicle z is at y, and not at x anymore.
  (:action travel-long
    :parameters (?x ?y ?z)
    :precondition (and
      (AIRPORT ?x)
      (AIRPORT ?y)
      (AIRPLANE ?z)
      (connected ?x ?y)
      (is-vehicle-at ?z ?x)
    )
    :effect (and
      (is-vehicle-at ?z ?y)
      (not (is-vehicle-at ?z ?x))
    )
  )

  ; Short-distance travel, i.e. not between airports, by a 
  ; subway train z if x and y are connected.
  ; As a result, vehicle z is at y, and not at x anymore.
  (:action travel-short
    :parameters (?x ?y ?z)
    :precondition (and
      (or (AIRPORT ?x) (STATION ?x))
      (or (AIRPORT ?y) (STATION ?y))
      (SUBWAY ?z)
      (connected ?x ?y)
      (is-vehicle-at ?z ?x)
    )
    :effect (and
      (is-vehicle-at ?z ?y)
      (not (is-vehicle-at ?z ?x))
    )
  )
)
