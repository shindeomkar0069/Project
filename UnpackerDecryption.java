import java.io.*;
import java.security.MessageDigest;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import javax.swing.*;

class UnpackerDecryption
{
    public static void main(String A[]) throws Exception
    {
        JFrame f = new JFrame("Decryption and Unpacking");

        JLabel l1 = new JLabel("Encrypted File");
        JLabel l2 = new JLabel("Password");

        JTextField t1 = new JTextField();
        JTextField t2 = new JTextField();

        JButton b = new JButton("Unpack");

        l1.setBounds(30, 30, 120, 30);
        t1.setBounds(150, 30, 250, 30);

        l2.setBounds(30, 80, 120, 30);
        t2.setBounds(150, 80, 250, 30);

        b.setBounds(160, 140, 100, 40);

        f.add(l1);
        f.add(t1);
        f.add(l2);
        f.add(t2);
        f.add(b);

        b.addActionListener(e ->
        {
            try
            {
                String PackFileName = t1.getText();
                String Password = t2.getText();

                File fpackobj = new File(PackFileName);

                if(!fpackobj.exists())
                {
                    JOptionPane.showMessageDialog(
                        f,
                        "Encrypted file does not exist"
                    );
                    return;
                }

                // -----------------------------
                // DECRYPTION
                // -----------------------------

                MessageDigest md = MessageDigest.getInstance("SHA-256");

                byte keyBytes[] = md.digest(Password.getBytes());

                SecretKeySpec key = new SecretKeySpec(keyBytes, "AES");

                Cipher cipher = Cipher.getInstance("AES");

                cipher.init( Cipher.DECRYPT_MODE, key);

                FileInputStream encryptedInput =  new FileInputStream(fpackobj);

                byte encryptedData[] = encryptedInput.readAllBytes();

                encryptedInput.close();

                byte decryptedData[] = cipher.doFinal(encryptedData);

                // Temporary decrypted packed file
                File decryptedFile = new File("DecryptedPack.tmp");

                FileOutputStream decryptedOutput = new FileOutputStream(decryptedFile);

                decryptedOutput.write(decryptedData);
                decryptedOutput.close();

                // -----------------------------
                // UNPACKING
                // -----------------------------

                FileInputStream fiobj =
                    new FileInputStream(decryptedFile);

                byte Header[] =
                    new byte[100];

                String strHeader = null;
                String Tokens[] = null;
                File NewFile = null;
                FileOutputStream foobj = null;
                byte Buffer[] = null;
                int iRet = 0;

                // Read header
                while((iRet =
                    fiobj.read(Header, 0, 100)) != -1)
                {
                    strHeader = new String(Header);

                    System.out.println(  "Header is : " + strHeader );

                    strHeader = strHeader.trim();

                    strHeader = strHeader.replaceAll("\\s+", " ");

                    Tokens = strHeader.split(" ");

                    System.out.println( "File name : " + Tokens[0]);

                    System.out.println( "File size : " + Tokens[1] );

                    NewFile = new File(Tokens[0]);

                    NewFile.createNewFile();

                    foobj =  new FileOutputStream(NewFile);

                    Buffer = new byte[ Integer.parseInt(Tokens[1]) ];

                    // Read data
                    fiobj.read( Buffer, 0,Integer.parseInt(Tokens[1]));

                    // Write data
                    foobj.write( Buffer, 0, Integer.parseInt(Tokens[1]) );

                    foobj.close();
                }

                fiobj.close();

                // Delete temporary decrypted file
                decryptedFile.delete();

                JOptionPane.showMessageDialog(f,  "Decryption and Unpacking Completed" );
            }
            catch(Exception ex)
            {
                JOptionPane.showMessageDialog(f,"Wrong password or invalid file");
            }
        });

        f.setSize(450, 240);
        f.setLayout(null);

        f.setDefaultCloseOperation(
            JFrame.EXIT_ON_CLOSE
        );

        f.setVisible(true);
    }
}
