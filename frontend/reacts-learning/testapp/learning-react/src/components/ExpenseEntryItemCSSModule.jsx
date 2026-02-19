import React from "react";
import styles from "./ExpenseEntryItemCSSModule.module.css";

class ExpenseEntryItemCSSModule extends React.Component {
  render() {
    return (
      <div className={styles.itemStyle}>
        <div>
          <b>Item:</b> <em>Mango Juice</em>
        </div>
        <div>
          <b>Amount:</b> <em>300.00</em>
        </div>
        <div>
          <b>Spend Date:</b> <em>2024-10-10</em>
        </div>
        <div>
          <b>Category:</b> <em>Food</em>
        </div>
      </div>
    );
  }
}
export default ExpenseEntryItemCSSModule;
