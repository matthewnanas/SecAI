import * as React from 'react';
import { StyleSheet } from 'react-native';
import { WebView } from 'react-native-webview';
import { Text, View } from '../components/Themed';

export default function TabTwoScreen() {
  var driveurl = 'https://drive.google.com';
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Recordings</Text>
      <WebView
          useWebKit={true} 
          startInLoadingState={true}
          automaticallyAdjustContentInsets={false}
          source={{uri: driveurl}}
          scalesPageToFit={true}
          bounces={false}
          javaScriptEnabled={false}
          originWhitelist={['*']}
          style={{ height: 500, width: 300, flex: 1 }}
        />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  separator: {
    marginVertical: 30,
    height: 1,
    width: '80%',
  },
});
