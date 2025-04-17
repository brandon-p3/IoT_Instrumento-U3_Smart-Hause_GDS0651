function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const nivel = data.nivel;
    const email = "natzllyuni@gmail.com";
    const timestamp = new Date().toLocaleString();
    
    // Determinar nivel de peligro y color correspondiente
    let nivelPeligro = "BAJO";
    let colorPeligro = "#FFC107"; // Amarillo
    
    if (nivel > 500) {
      nivelPeligro = "CRÍTICO";
      colorPeligro = "#DC3545"; // Rojo
    } else if (nivel > 300) {
      nivelPeligro = "ALTO";
      colorPeligro = "#FF5722"; // Naranja
    }
    
    // Crear HTML para email con mejor formato
    const htmlBody = `
      <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #ddd; border-radius: 5px; overflow: hidden;">
        <div style="background-color: ${colorPeligro}; color: white; padding: 15px; text-align: center;">
          <h1 style="margin: 0; font-size: 24px;">🚨 ALERTA DE GAS DETECTADA 🚨</h1>
        </div>
        
        <div style="padding: 20px;">
          <p style="font-size: 16px;"><strong>Dispositivo:</strong> Sensor de Gas MQ-2</p>
          <p style="font-size: 16px;"><strong>Ubicación:</strong> Casa</p>
          
          <div style="background-color: #f5f5f5; border-radius: 5px; padding: 15px; margin: 20px 0;">
            <table style="width: 100%; border-collapse: collapse;">
              <tr>
                <td style="padding: 10px 0;"><strong>Nivel de gas detectado:</strong></td>
                <td style="font-weight: bold; color: ${colorPeligro};">${nivel} PPM</td>
              </tr>
              <tr>
                <td style="padding: 10px 0;"><strong>Nivel de peligro:</strong></td>
                <td style="font-weight: bold; color: ${colorPeligro};">${nivelPeligro}</td>
              </tr>
              <tr>
                <td style="padding: 10px 0;"><strong>Fecha y hora:</strong></td>
                <td>${timestamp}</td>
              </tr>
            </table>
          </div>
          
          <div style="background-color: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p style="margin: 0;"><strong>Acciones recomendadas:</strong></p>
            <ul style="margin-top: 10px;">
              <li>Abra las ventanas para ventilar el área</li>
              <li>No encienda luces ni aparatos eléctricos</li>
              <li>Evacúe el área si el nivel es crítico</li>
              <li>Llame a emergencias si el nivel es alto o crítico</li>
            </ul>
          </div>
          
          <p style="font-size: 14px; color: #666; text-align: center; margin-top: 30px;">
            Este es un mensaje automático generado por su sistema de seguridad de gas.
            <br>No responda a este correo.
          </p>
        </div>
        
        <div style="background-color: #f5f5f5; padding: 15px; text-align: center; font-size: 12px; color: #666;">
          © Sistema de Monitoreo de Gas Doméstico ${new Date().getFullYear()}
        </div>
      </div>
    `;
    
    // Versión de texto plano como respaldo
    const plainBody = 
      "🚨 ¡ALERTA DE GAS DETECTADO!\n\n" +
      "Sensor: MQ-2\n" +
      "Nivel de gas: " + nivel + " PPM\n" +
      "Nivel de peligro: " + nivelPeligro + "\n" +
      "Hora: " + timestamp + "\n\n" +
      "ACCIONES RECOMENDADAS:\n" +
      "- Abra las ventanas para ventilar el área\n" +
      "- No encienda luces ni aparatos eléctricos\n" +
      "- Evacúe el área si el nivel es crítico\n" +
      "- Llame a emergencias si el nivel es alto o crítico";
    
    // Enviar email con HTML y respaldo en texto plano
    MailApp.sendEmail({
      to: email,
      subject: `🚨 ALERTA DE GAS ${nivelPeligro} - Acción Requerida`,
      htmlBody: htmlBody,
      body: plainBody
    });
    
    return ContentService.createTextOutput(JSON.stringify({
      status: "success",
      message: "Alerta enviada correctamente"
    })).setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: error.message
    })).setMimeType(ContentService.MimeType.JSON);
  }
}