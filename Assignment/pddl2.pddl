;; Problem definition
(define (problem problem-2)

  ;; Specifying the domain for the problem
  (:domain travel-domain)

  ;; Objects definition
  (:objects
    ; airports
    AP1 AP2 AP3
    ; stations
    S11 S12 S21 S22 S31
    ; persons
    person1 person2
    ; vehicles
    plane1 plane2 train1 train2 train3
  )

  ;; Initial state of the problem
  (:init
    ;; Declaration of the objects
    ; Airports
    (AIRPORT AP1)
    (AIRPORT AP2)
    (AIRPORT AP3)
    ; Stations
    (STATION S11)
    (STATION S12)
    (STATION S21)
    (STATION S22)
    (STATION S31)
    ; Persons
    (PERSON person1)
    (PERSON person2)
    ; Vehicles
    (VEHICLE plane1)
    (VEHICLE plane2)
    (VEHICLE train1)
    (VEHICLE train2)
    (VEHICLE train3)
    (AIRPLANE plane1)
    (AIRPLANE plane2)
    (SUBWAY train1)
    (SUBWAY train2)
    (SUBWAY train3)
    
    ; Links (Connections)
    (connected AP1 AP2) (connected AP2 AP1)
    (connected AP2 AP3) (connected AP3 AP2)
    (connected S11 S12) (connected S12 S11)
    (connected AP1 S11) (connected S11 AP1)
    (connected AP1 S12) (connected S12 AP1)
    (connected AP2 S21) (connected S21 AP2)
    (connected AP2 S22) (connected S22 AP2)
    (connected AP3 S31) (connected S31 AP3)
    
    ;; Declaration of the predicates of the objects
    ; Vehicle Locations
    (is-vehicle-at plane1 AP1)
    (is-vehicle-at plane2 AP3)
    (is-vehicle-at train1 S12)
    (is-vehicle-at train2 AP2)
    (is-vehicle-at train3 S31)
    
    ; Person Locations
    (is-person-at person1 S11)
    (is-person-at person2 S31)
  )

  ;; Goal specification
  (:goal
    (and
      ; Goals for person1 and person2
      (is-person-at person1 S21)
      (is-person-at person2 S12)
    )
  )
)
