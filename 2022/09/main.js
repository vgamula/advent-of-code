const fs = require('fs');

const coordStr = ({ x, y }) => x.toString() + ' ' + y.toString();

const areClose = (head, tail) => (
  Math.abs(head.x - tail.x) <= 1 &&
  Math.abs(head.y - tail.y) <= 1
);

const directions = {
  'R': [1, 0],
  'L': [-1, 0],
  'U': [0, 1],
  'D': [0, -1],
};

const solve = (commands, ropeLength) => {
  const rope = [...Array(ropeLength).keys()].map(_ => ({ x: 0, y: 0 }));
  const tailVisitedCoords = new Set([coordStr(rope[ropeLength - 1])]);

  commands.forEach(([direction, count]) => {
    const [dx, dy] = directions[direction];

    while (count-- > 0) {
      rope[0].x += dx;
      rope[0].y += dy;

      for (let i = 1; i < ropeLength; i++) {
        const head = rope[i - 1];
        const tail = rope[i];
        if (areClose(head, tail)) {
          break;
        }
        tail.x += Math.sign(head.x - tail.x);
        tail.y += Math.sign(head.y - tail.y);
      }

      tailVisitedCoords.add(coordStr(rope[ropeLength - 1]));
    }
  });

  return tailVisitedCoords.size;
};


const commands = fs.readFileSync('input.txt', 'utf8')
  .split('\n')
  .map(x => x.split(' '));

console.log('Task 1:', solve(commands, 2));
console.log('Task 2:', solve(commands, 10));
