import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({

  container: {
    flex: 1,
    backgroundColor: 'white',
    alignItems: 'center',
    justifyContent: 'center',
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
    backgroundColor: '#a17d3b',
    color: '#fff',
    padding: 12,
  },

  esqueceuSenha: {
    marginLeft: 30,
    color: '#000000',
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
  },

  colunaTopo: {
    position: 'absolute',
    top: 0,
    alignSelf: 'center',
  },

  colunaRodape: {
    position: 'absolute',
    alignSelf: 'center',
    bottom: 0,
  },

});

export default styles;