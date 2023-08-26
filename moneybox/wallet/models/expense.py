from django.db import models, transaction

from users.models import Profile
from wallet.models.group import Group
from wallet.models.timestamp import TimestampMixin
from wallet.models.wallet import Wallet


class ExpenseCategory(TimestampMixin):
    name = models.CharField(
        max_length=255,
        verbose_name="Name",
        help_text="The name of the expense category",
        db_index=True,
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name="Group",
        help_text="The group this expense category belongs to",
        db_index=True,
    )
    created_by = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        verbose_name="User",
        help_text="The user who created this expense category",
    )

    class Meta:
        verbose_name = "Expense Category"
        verbose_name_plural = "Expense Categories"


class Expense(TimestampMixin):
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount of expense")
    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.CASCADE,
        verbose_name="Expense category",
        db_index=True,
    )
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="Comment on expense")
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="User who made the expense")
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        verbose_name="Wallet used for the expense",
        db_index=True,
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name="Group related to the expense",
        db_index=True,
    )

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"

    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.wallet.balance -= self.amount
        self.wallet.save()