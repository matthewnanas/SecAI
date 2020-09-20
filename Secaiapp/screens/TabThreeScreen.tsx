import * as React from 'react';
import { TextInput, Button, StyleSheet } from 'react-native';
//import { TextInput } from 'react-native-gesture-handler';
import { WebView } from 'react-native-webview';
//import EditScreenInfo from '../components/EditScreenInfo';
import { Text, View } from '../components/Themed';
import Textarea from 'react-native-textarea';

class TabThreeSecreen extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      numbers: '',
    }
  }
  updateContacts = () => {
    var numbers = this.state.numbers;
    numbers.replace(/\n/g, ",")
    //alert(numbers);
    try {
      let response = fetch(
        "http://localhost:1337/numbers",
        {
          method: 'post',
          body: numbers,
        },
      )
    } catch (error) {
      alert(error);
    }
  }

  render() {
    const styles = StyleSheet.create({
      textAreaContainer: {
        borderColor: 'grey',
        marginTop: 35,
        borderWidth: 1,
        padding: 5,
        height: '70%',
      },
      textArea: {
        marginTop: 30,
        height: '90%',
        justifyContent: "flex-start"
      }
    });
    return (
      <View style={styles.textAreaContainer} >
        <TextInput
          ref = "numbers"
          underlineColorAndroid="transparent"
          placeholder="XXXXXXXXXX"
          placeholderTextColor="grey"
          value = {this.state.numbers}
          onChangeText = {numbers => this.setState({numbers})}
          numberOfLines={10}
          multiline={true}
        />
        <Button
          title="Update"
          color="#0562f7"
          style={{marginVertical: 100}}
          
          onPress={this.updateContacts.bind(this)}
        />
      </View>
      );
  }
}

export default TabThreeSecreen

/*export default function TabOneScreen() {
  const [value, defaultText] = React.useState('XXXXXXXXXX');
  text = '';
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Contact List</Text>
      <Textarea
        style={{height: '50%', width: "85%", marginLeft: "7.5%",}}
        placeholder={'XXXXXXXXXX'}
        onChange={text => }
        placeholderTextColor={'#c7c7c7'}
        underlineColorAndroid={'transparent'}
      />
      <Button
          title="Update"
          color="#0562f7"
          style={{marginVertical: 100}}
          onPress={() => alert('test')}
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
});*/
