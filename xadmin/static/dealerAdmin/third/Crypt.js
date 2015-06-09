  
var AESEncryptUtf8StrBase64 = function(text, pass, iv) {
    passtr = CryptoJS.enc.Latin1.parse(pass);
    ivstr = CryptoJS.enc.Latin1.parse(iv);
    txtstr = CryptoJS.enc.Base64.stringify(CryptoJS.enc.Utf8.parse(text));

    var encrypted = CryptoJS.AES.encrypt(
            txtstr,
            passtr, 
            {iv: ivstr, mode: CryptoJS.mode.CFB, padding: CryptoJS.pad.ZeroPadding}
        );

    return encrypted.toString();   
};

var AESDecryptUtf8StrBase64 = function(cipherstr, pass, iv) {
    passtr = CryptoJS.enc.Latin1.parse(pass);
    ivstr = CryptoJS.enc.Latin1.parse(iv);

    cipher = CryptoJS.lib.CipherParams.create(
                {ciphertext: CryptoJS.enc.Base64.parse(cipherstr)}
             );
    var decrypted = CryptoJS.AES.decrypt(
            cipher, 
            passtr, 
            {iv : ivstr, mode: CryptoJS.mode.CFB, padding: CryptoJS.pad.ZeroPadding}
         );
    var base64txt = decrypted.toString(CryptoJS.enc.Utf8);
    return CryptoJS.enc.Base64.parse(base64txt).toString(CryptoJS.enc.Utf8);
};

