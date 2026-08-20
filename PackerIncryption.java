import java.io.*;
import java.security.MessageDigest;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import javax.swing.*;

class PackerIncryption
{
    public static void main(String A[]) throws Exception
    {
        JFrame f = new JFrame("Packing and Encryption");

        JLabel l1 = new JLabel("Folder Name");
        JLabel l2 = new JLabel("Packed File");
        JLabel l3 = new JLabel("Password");

        JTextField t1 = new JTextField();
        JTextField t2 = new JTextField();
        JTextField t3 = new JTextField();

        JButton b = new JButton("Pack");

        l1.setBounds(30,30,100,30);
        t1.setBounds(140,30,250,30);

        l2.setBounds(30,80,100,30);
        t2.setBounds(140,80,250,30);

        l3.setBounds(30,130,100,30);
        t3.setBounds(140,130,250,30);

        b.setBounds(160,180,100,40);

        f.add(l1);
        f.add(t1);
        f.add(l2);
        f.add(t2);
        f.add(l3);
        f.add(t3);
        f.add(b);

        b.addActionListener(e ->
        {
            try
            {
                int iRet = 0;
                int Size = 0;
                int i = 0, j = 0;

                String FolderName = t1.getText();
                String PackFileName = t2.getText();
                String Password = t3.getText();
                String header = "";

                FileOutputStream foobj = null;
                FileInputStream fiobj = null;

                byte Buffer[] = new byte[1024];
                byte bHeader[] = null;

                File fobjfolder =
                    new File(FolderName);

                if((fobjfolder.exists()) &&
                   (fobjfolder.isDirectory()))
                {
                    File fobjpack =new File(PackFileName);

                    fobjpack.createNewFile();

                    foobj = new FileOutputStream(fobjpack);

                    File fArr[] = fobjfolder.listFiles();

                    ////////////// PACKING //////////////

                    for(i = 0; i < fArr.length; i++)
                    {
                        if(fArr[i].isFile() &&
                          (fArr[i].getName().endsWith(".txt") ||
                           fArr[i].getName().endsWith(".c") ||
                           fArr[i].getName().endsWith(".cpp")))
                        {
                            fiobj =  new FileInputStream(fArr[i]);

                            header = fArr[i].getName();

                            header =  header + " ";

                            header = header + fArr[i].length();

                            Size = 100 - header.length();

                            for(j = 1; j <= Size; j++)
                            {
                                header =  header + " ";
                            }

                            bHeader = header.getBytes();

                            // Write header
                            foobj.write(bHeader);

                            // Write file data
                            while((iRet = fiobj.read(Buffer)) != -1)
                            {
                                foobj.write(
                                    Buffer,
                                    0,
                                    iRet);
                            }

                            fiobj.close();

                            header = "";
                        }
                    }

                    // Packing completed
                    foobj.close();

                    ////////////// ENCRYPTION //////////////

                    MessageDigest md = MessageDigest.getInstance("SHA-256");

                    byte keyBytes[] = md.digest( Password.getBytes());

                    SecretKeySpec key = new SecretKeySpec(keyBytes, "AES");

                    Cipher cipher = Cipher.getInstance("AES");

                    cipher.init( Cipher.ENCRYPT_MODE, key);

                    // Read entire packed file
                    FileInputStream fin =  new FileInputStream(PackFileName);

                    byte data[] = fin.readAllBytes();

                    fin.close();

                    // Encrypt all data at once
                    byte encrypted[] = cipher.doFinal(data);

                    // Create .enc file
                    FileOutputStream enc =  new FileOutputStream(PackFileName + ".enc");

                    enc.write(encrypted);

                    enc.close();

                    // Delete temporary packed file
                    new File(PackFileName).delete();

                    JOptionPane.showMessageDialog(f, "Packing and Encryption Completed\n" + "File : " + PackFileName + ".enc");
                }
                else
                {
                    JOptionPane.showMessageDialog( f, "There is no such folder");
                }
            }
            catch(Exception ex)
            {
                JOptionPane.showMessageDialog( f, ex.getMessage());
            }
        });

        f.setSize(450,300);
        f.setLayout(null);
        f.setDefaultCloseOperation( JFrame.EXIT_ON_CLOSE);
        f.setVisible(true);
    }
}