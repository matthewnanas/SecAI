import * as React from 'react';
import { StyleSheet } from 'react-native';
import { WebView } from 'react-native-webview';
//import EditScreenInfo from '../components/EditScreenInfo';
import { Text, View } from '../components/Themed';

export default function TabTwoScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Recordings</Text>
      <WebView
          scalesPageToFit={true}
          bounces={false}
          javaScriptEnabled
          style={{ height: 500, width: 300 }}
          source={{
            html: `
            <iframe src="https://drive.google.com"
            title="iframe Example 1" width="100%" height="100%">
            </iframe>
            `,
          }}
          automaticallyAdjustContentInsets={false}
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
