import React, { useState } from 'react';

const AddBlock = () => {

    const [transactions, setTransactions] = useState([
        [{ key: 'Sender', value: '' }, { key: 'Recipient', value: '' }, { key: 'Amount', value: '' }, { key: 'Timestamp', value: new Date().toLocaleString()}],
      ]);
    
      const addTransactionField = (index) => {
        const newTransactions = [...transactions];
        newTransactions[index].push({ key: '', value: '' });
        setTransactions(newTransactions);
      };
    
      const handleFieldChange = (transactionIndex, fieldIndex, part, value) => {
        const updatedTransactions = transactions.map((transaction, tIndex) => {
          if (tIndex === transactionIndex) {
            return transaction.map((field, fIndex) => {
              if (fIndex === fieldIndex) {
                return { ...field, [part]: value };
              }
              return field;
            });
          }
          return transaction;
        });
        setTransactions(updatedTransactions);
      };
    
      // todo: logic to send shit to block chain / database
      const addTransaction = () => {
        setTransactions([...transactions, [{ key: 'sender', value: '' }, { key: 'recipient', value: '' }, { key: 'amount', value: '' }]]);
      };

      return (
        <div className="flex flex-col h-screen p-4">
          <header className="flex justify-between items-center">
            <h1 className="text-2xl font-bold">Blockchain</h1>
            <span>{new Date().toLocaleString()}</span>
          </header>
    
          <div className="flex-grow overflow-auto">
            {transactions.map((transaction, tIndex) => (
              <div key={tIndex} className="bg-white p-6 shadow rounded-lg my-4 max-w-2xl mx-auto">
                <h2 className="text-lg font-semibold mb-4">Transaction {tIndex + 1}</h2>
                {transaction.map((field, fIndex) => (
                  <div key={fIndex} className="mb-4 flex space-x-2">
                    <input
                      type="text"
                      value={field.key}
                      onChange={(e) => handleFieldChange(tIndex, fIndex, 'key', e.target.value)}
                      placeholder="Field Name"
                      className="border p-2 flex-grow"
                    />
                    <input
                      type="text"
                      value={field.value}
                      onChange={(e) => handleFieldChange(tIndex, fIndex, 'value', e.target.value)}
                      placeholder="Field Value"
                      className="border p-2 flex-grow"
                    />
                  </div>
                ))}
                <button
                  onClick={() => addTransactionField(tIndex)}
                  className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
                >
                  + Add Field
                </button>
              </div>
            ))}
    
            <div className="flex justify-center items-center p-4">
              <button onClick={addTransaction} className="bg-green-500 text-white p-3 rounded hover:bg-green-600">
                + Add Transaction
              </button>
            </div>
          </div>
    
        {/* Need button that will post transactions to blockchaiin   */}
        </div>
      );
}

export default AddBlock;