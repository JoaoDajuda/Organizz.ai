import { StyleSheet, ScrollView, Image, Text, View, SafeAreaView, TextInput, TouchableOpacity} from 'react-native';

export default function Organizzai() {
  return (
  <SafeAreaView style={styles.container}>
    <Image source={require('./assets/colunaCinza.png')} />
    <Image style={styles.logo} source={require('./assets/logo.png')}></Image>
    <TextInput style={styles.input} placeholder="Digite seu email:" placeholderTextColor="#fff"></TextInput>
    <TextInput style={styles.input} placeholder="Digite sua senha:" placeholderTextColor="#fff"></TextInput>
    <TouchableOpacity>
      <Text>Esqueceu sua senha?</Text>
    </TouchableOpacity>
    <Image source={require('./assets/colunaCinza.png')} />
  </SafeAreaView>
  )
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#D4AF6A',
    alignItems: 'center',
    justifyContent: 'center',
  },
  logo: {
    width: 150,
    height: 100,
  },
  input: {
    width: 250,
    margin: 5,
    borderRadius: 5,
    backgroundColor: '#4A4540',
    color: '#fff',
    padding: 12,
}
});
