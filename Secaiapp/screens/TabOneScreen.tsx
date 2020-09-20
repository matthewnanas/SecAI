import * as React from 'react';
import { StyleSheet } from 'react-native';
import { WebView } from 'react-native-webview';
//import EditScreenInfo from '../components/EditScreenInfo';
import { Text, View } from '../components/Themed';

export default function TabOneScreen() {
  // USE IP OF STREAMING DEVICE
  var ipurl = 'http://192.168.1.153:9218/';
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Live Feed</Text>
        <WebView
          automaticallyAdjustContentInsets={false}
          source={{uri: ipurl}}
          scalesPageToFit={true}
          bounces={false}
          javaScriptEnabled
          style={{ height: 1500, width: 900 }}
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
