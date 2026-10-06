export function parseBenchmarkDashboard(htmlString: string) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(htmlString, 'text/html');
  const scores: Array<{ vendor: string; score: number }> = [];

  doc.querySelectorAll('.benchmark-score').forEach((el) => {
    const vendor = el.querySelector('.vendor')?.textContent ?? '';
    const scoreText = el.querySelector('.score')?.textContent ?? '0';
    const score = parseFloat(scoreText) || 0;
    scores.push({ vendor, score });
  });

  return scores;
}
