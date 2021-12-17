<?php
$input = array_map(fn($x) => (int)$x, explode(",", trim(fgets(STDIN))));

$state = array_count_values($input);

function step($state) {
  $new_state = array();
  foreach ($state as $age => $fish_cnt) {
    if ($age == 0) {
      $new_state[8] += $fish_cnt;
      $new_state[6] += $fish_cnt;
    } else {
      $new_state[$age - 1] += $fish_cnt;
    }
  }
  return $new_state;
}

function simulate($state, $days) {
  for ($i = 0; $i < $days; $i++) {
    $state = step($state);
  }
  return $state;
}

function population($state) {
  return array_sum($state);
}


echo "\n18 days: " . population(simulate($state, 18));
echo "\nTask 1: " . population(simulate($state, 80));
echo "\nTask 2: " . population(simulate($state, 256));
?>