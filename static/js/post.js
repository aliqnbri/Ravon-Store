async function makePostRequest(path, requestData) {
    try {
      const response = await axios.post(path, requestData);
      return response.data;
    } catch (error) {
      console.error('Error occurred:', error);
      throw new Error('Error occurred while making POST request');
    }
  }
  