import { StyleSheet, Image, Text, View, SafeAreaView, TextInput, TouchableOpacity, Button} from 'react-native';

export default function Organizzai() {
  return (
    <SafeAreaView style={styles.container}>
    <Image style={styles.coluna_topo} source={require('./assets/colunaInvertidaCinza.png')} />
    <View style={styles.formContainer}>
      <Image style={styles.logo} source={require('./assets/logoDourada.png')}></Image>
      <View style={styles.containerinputs}>
        <TextInput style={styles.input} placeholder="Digite seu email:" placeholderTextColor="#fff"></TextInput>
        <TextInput style={styles.input} placeholder="Digite sua senha:" placeholderTextColor="#fff"></TextInput>
      </View>
      <TouchableOpacity>
        <Text style={{color: '#fff'}}>Esqueceu sua senha?</Text>
      </TouchableOpacity>
      <View style={styles.viewBotao}>
        <Button style={styles.botao} color={'#4A4540'} title="Login" onPress={() => {}} />
      </View>
    </View>
    <Image style={styles.coluna_rodape} source={require('./assets/colunaCinza.png')} />
  </SafeAreaView>
  )
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1C1717',
    alignItems: 'center',
    justifyContent: 'center'
  },
  formContainer: {    
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  containerInputs: {
    marginTop: 20,
  },
  logo: {
    width: 200,
    height: 180,
  },
  input: {
    width: 250,
    margin: 5,
    borderRadius: 5,
    backgroundColor: '#4A4540',
    color: '#fff',
    padding: 12,
},
  viewBotao: {    
    marginTop: 20,
    marginLeft: 125,
  },
  botao: {
    borderRadius: 15,
    backgroundColor: '#4A4540',
    color: '#fff',
    padding: 12,
    marginLeft: 20,
    hover: '#373330',
  },
  coluna_topo: {
    position: 'absolute',
    top: '0',
    alignSelf: 'center',
  },
  coluna_rodape: {
    position: 'absolute',
    alignSelf: 'center',
    bottom: '0'
  },
});