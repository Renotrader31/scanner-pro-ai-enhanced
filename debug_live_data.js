// Debug script to test live data functionality
console.log('🔬 Live Data Debug Script Started');

// Check if all functions exist
console.log('🔍 Checking function availability...');
console.log('switchToLiveData function exists:', typeof switchToLiveData);
console.log('dataManager exists:', typeof dataManager);
console.log('API_CONFIG exists:', typeof API_CONFIG);

if (typeof API_CONFIG !== 'undefined') {
    console.log('📊 API_CONFIG contents:', API_CONFIG);
} else {
    console.error('❌ API_CONFIG is not defined!');
}

if (typeof dataManager !== 'undefined') {
    console.log('📊 dataManager contents:', dataManager);
    console.log('📊 dataManager.enableLiveData exists:', typeof dataManager.enableLiveData);
} else {
    console.error('❌ dataManager is not defined!');
}

// Test the button click manually
console.log('🔄 Attempting to trigger live data activation...');

if (typeof switchToLiveData !== 'undefined') {
    console.log('✅ switchToLiveData function found, calling it...');
    switchToLiveData().then(() => {
        console.log('✅ switchToLiveData completed successfully');
    }).catch((error) => {
        console.error('❌ switchToLiveData failed:', error);
    });
} else {
    console.error('❌ switchToLiveData function not found!');
}

console.log('🔬 Debug script execution completed');