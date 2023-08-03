const fs = require('fs');
const csvPath = process.argv[2]

function csvToJson(csv) {
  const lines = csv.split('\n');
  const headers = lines[0].split(',');
  const jsonData = [];

  for (let i = 1; i < lines.length; i++) {
    if (lines[i].trim() === '') continue;
    let singleRow = {};
    for (let j = 0; j < headers.length; j++) {
      singleRow[headers[j]] = lines[i].split(',')[j];
    }
    jsonData.push(singleRow);
  }
  return jsonData;
}

fs.readFile(csvPath, 'utf-8', (error, csvData) => {
  if (error) {
    console.log('Error', error);
    return 0;
  }

  const jsonData = csvToJson(csvData);
  const jsonString = JSON.stringify(jsonData, null, 2);
  const start = performance.now()
  console.log(jsonString);
  const end = performance.now();

  console.log("time took to convert csv into JSON: ",end - start);
});
