import {  Image,  Text,  View,  TextInput,  TouchableOpacity,  Button} from 'react-native';
import styles from './stylesLogin';

export default function Login() {

  return (
    <View style={styles.container}>

      <View style={styles.formContainer}>

        <Image
          style={styles.logo}
          source={require('../../../assets/logoBranco2.jpeg')}
        />

        <View style={styles.containerInputs}>

          <TextInput
            style={styles.input}
            placeholder="Digite seu email:"
            placeholderTextColor="#fff"
          />

          <TextInput
            style={styles.input}
            placeholder="Digite sua senha:"
            placeholderTextColor="#fff"
          />

        </View>

        <TouchableOpacity>
          <Text style={styles.esqueceuSenha}>
            Esqueceu sua senha?
          </Text>
        </TouchableOpacity>

        <View style={styles.viewBotao}>
          <Button
            color="#4A4540"
            title="LOGIN"
            onPress={() => {}}
          />
        </View>

      </View>

    </View>
  );
};