// Source - https://stackoverflow.com/q
// Posted by Kristopher Johnson, modified by community. See post 'Timeline' for change history
// Retrieved 2025-11-28, License - CC BY-SA 4.0

var testObject = { 'one': 1, 'two': 2, 'three': 3 };
console.log('typeof testObject: ' + typeof testObject);
console.log('testObject properties:');
for (var prop in testObject) {
    console.log('  ' + prop + ': ' + testObject[prop]);
}

// Put the object into storage
localStorage.setItem('testObject', testObject);

// Retrieve the object from storage
var retrievedObject = localStorage.getItem('testObject');

console.log('typeof retrievedObject: ' + typeof retrievedObject);
console.log('Value of retrievedObject: ' + retrievedObject);
console.log('Reload complete');